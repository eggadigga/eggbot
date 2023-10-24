#! python3

'''
name: real_trader_egg.py
description: trade bot placing random trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_real import AlpacaReal
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
real_api_key = os.environ['apcarealkey']
real_api_secret = os.environ['apcarealsecret']
exchange = AlpacaReal(real_api_key, real_api_secret)

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
        if pnl_pct.startswith(('0.0000', '-0.0000')) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) < -0.03:
           exchange.close_single_position(symbol)
        elif pnl_pct.startswith(('0.0000', '-0.0000')) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.07:
            exchange.close_single_position(symbol)
        else:
            continue
def account_balance():
    equity = exchange.get_account_info()['equity']
    cash = exchange.get_account_info()['cash']
    now = datetime.now()
    print(f'\n\n|| Current Account Balance as of {now} ||')
    print(f'equity: {equity}')
    print(f'cash: {cash}')

def get_most_active_stocks():
 #### Get Top 20 Most Traded Stocks  ####
    avmd = AlphaVantage(os.environ['alphavantkey'])
    symbols = []
    for sym in avmd.get_top_20_gla()['most_actively_traded']:
        if int(float(sym['price'])) <= 20:
            symbols.append(sym['ticker'])
    return symbols
    
if __name__ == '__main__':
    print()
    print('$'*75)
    print('\nEgga\'s stock trading bot is now running.')
    print('Author: eggadigga\n')
    print('$'*75)

    while True:
    #### Loop until market opens
        if exchange.get_market_clock()['is_open'] == False:
            while exchange.get_market_clock()['is_open'] == False:
                account_balance()
                print('\nMarket is currently closed...\n')
                sleep(60)
        print('\nMarket is now open... Let the games begin...')
        sleep(600)

    #### Buy stocks first thing in the morning per config file ####
        config.read(config_file, encoding='utf-8')
        buy_am = config['trade_env']['buy_am']
        if  buy_am == 'yes':
            symbols = get_most_active_stocks()
            buy_stock_market_order(symbols)
            
    #### Prevent pattern day trade by waiting until market close and reopen.
            while exchange.get_market_clock()['is_open'] == True:
                account_balance()
                sleep(60)
            sleep(2)
            while exchange.get_market_clock()['is_open'] == False:
                account_balance()
                print('\nMarket is currently closed...\n')
                sleep(60)

    #### Gather current time, set sell time to 1:30 PM ET.
    #### While loop analyzing positions throughout day, and sell based on unrealized pnl.
    #### If current time is > 1:30 PM ET, loop breaks and all positions are sold.
        current_time = datetime.now().time()
        close_all_positions_time = time(hour=13, minute=30)
        while current_time < close_all_positions_time:
            analyze_positions()
            current_time = datetime.now().time()
            account_balance()
            sleep(60)
        for position in exchange.get_open_positions():
            if position['asset_class'] == 'us_equity':
                exchange.close_single_position(position['symbol'])
                sleep(1)
            else:
                continue

    #### Open New Positions after 1:30PM ET
        symbols = get_most_active_stocks()
        buy_stock_market_order(symbols)

    #### Cancel open orders
        sleep(20)
        exchange.cancel_order_list()

    #### Wait for market to close before returning to beginning
        while exchange.get_market_clock()['is_open'] == True:
            account_balance()
            sleep(60)
