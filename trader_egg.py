#! python3

'''
name: trader_egg.py
description: trade bot placing random trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_paper import AlpacaPaper
from modules.av_market_data import AlphaVantage
from pprint import pformat
import os, sys
from datetime import datetime, time, timedelta
from time import sleep

## environment configuration
main_dir = os.path.dirname(__file__)
config_dir = main_dir + '/config'
config_file = config_dir + '/config.ini'
env_file = config_dir + '/.env'
stock_symbols_file = config_dir + '/stock_symbols.txt'
config = ConfigParser()
config.read(config_file, encoding='utf-8')
load_dotenv(env_file)

## Stock symbols
symbol_list = [sym.split('\n')[0] for sym in open(stock_symbols_file).readlines()]

## Alpaca Instance Setup
paper_api_key = os.environ['apcapaperkey']
paper_api_secret = os.environ['apcapapersecret']
exchange = AlpacaPaper(paper_api_key, paper_api_secret)

## Get asset data from stock symbols in text file
def get_asset_info():
    asset_data_list = []
    for sym in symbol_list:
        asset = exchange.get_single_asset(sym)
        asset_data_list.append(asset)
    return asset_data_list

def buy_stock_trail_stop_order(amount, percentage):
    for sym in symbol_list:
        resp = exchange.buy_order_trail_stop(sym, amount, percentage)

def buy_stock_limit_order(amount, limit):
    for sym in symbol_list:
        resp = exchange.buy_order_limit(sym, amount, limit)

def buy_stock_market_order(symbols):
    ## Gather available cash
    account_data = exchange.get_account_info()
    cash = int(account_data['cash'].split('.')[0])
    ## Divide total cash by number of stocks to buy to get allotted cash for each stock.
    cash_alllotted_per_stock = int(cash / len(symbols)) 
    for sym in symbols:
        ## Get current bid for stock
        try:
            bid = exchange.get_latest_stock_quote(sym, os.environ['apcarealkey'], os.environ['apcarealsecret'])['quote']['bp']
            shares = str(int(cash_alllotted_per_stock / bid))
            resp = exchange.buy_order_market(sym, shares)
        except ZeroDivisionError as e:
            print(f'Error: {e}')

def analyze_positions():
    ## analyze open positions and close based on p/l.
    positions = exchange.get_open_positions()
    for position in positions:
        symbol = position['symbol']
        pnl_pct = position['unrealized_plpc']
        if pnl_pct.startswith(('0.0000', '-0.0000')) == False and float(pnl_pct) < -0.02:
           exchange.close_single_position(symbol)
        elif pnl_pct.startswith(('0.0000', '-0.0000')) == False and float(pnl_pct) > 0.07:
            exchange.close_single_position(symbol)
        else:
            continue
    
if __name__ == '__main__':

#### Loop until market opens
    while exchange.get_market_clock()['is_open'] == False:
        sleep(60)
        continue
          
#### Get Top 20 Most Traded Stocks  ####
    avmd = AlphaVantage(os.environ['alphavantkey'])
    symbols = []
    for sym in avmd.get_top_20_gla()['most_actively_traded']:
        if int(float(sym['price'])) <= 20:
            symbols.append(sym['ticker'])

#### Buy stocks ####
    # buy_stock_trail_stop_order('10', '3')
    # buy_stock_limit_order('10', '6')
    buy_stock_market_order(symbols)
    sleep(10)

#### Gather current time, set sell time to 3:53 PM ET.
#### While loop analyzing positions throughout day, and sell based on unrealized pnl.
#### If current time is > 3:53 PM ET, loop breaks and all positions are sold.
    current_time = datetime.now().time()
    close_all_positions_time = time(hour=15, minute=55)
    while current_time < close_all_positions_time:
        analyze_positions()
        current_time = datetime.now().time()
        sleep(60)
    exchange.close_all_positions()

### Get open orders
    #orders = exchange.get_order_list()
    # for order in orders:
    #     print(order['created_at'])
    #     print(order['symbol'])
    #     print(order['order_type'])
    #     print()

### Cancel orders
    #exchange.cancel_order_list()
