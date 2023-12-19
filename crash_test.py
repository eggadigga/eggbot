#! python3

'''
name: real_trader_egg.py
description: trade bot placing random trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_real import AlpacaReal
from pprint import pformat
import os, sys, socket, requests, random
from datetime import datetime, time, timedelta
from time import sleep
from modules.emailTool import sendMail

## environment configuration
main_dir = os.path.dirname(__file__)
config_dir = main_dir + '/config'
config_file = config_dir + '/config.ini'
env_file = config_dir + '/.env'
config = ConfigParser()
config.read(config_file, encoding='utf-8')
load_dotenv(env_file)

## Program failure notification
def app_fail_smtp_alert(errmsg):
    hostname = socket.gethostname()
    prv_ipaddr = socket.gethostbyname(hostname)
    pub_ipaddr = requests.get('http://ipinfo.io/ip', verify=False).text
    mailusr = 'alerts.digga@gmail.com'
    mailpw = os.getenv('mailpw')
    sender = 'Ed Reyes <alerts.digga@gmail.com>'
    receivers = ['eggadigga19@gmail.com']
    cc = ['egga19@yahoo.com', 'eduardo.reyes120@gmail.com']
    server = 'smtp.gmail.com'
    sub = f'{hostname} - Eggadigga Stock Trade Bot Stopped Running'
    body = f'''
Bot stopped running unexpectedly

Source hostname: {hostname}
Internal IP: {prv_ipaddr}
Public IP: {pub_ipaddr}

Reason: {errmsg}
    '''
    sendMail(sender, receivers, cc, sub, body, mailusr, mailpw, server)

## Alpaca Instance Setup
real_api_key = os.environ['apcarealkey']
real_api_secret = os.environ['apcarealsecret']
exchange = AlpacaReal(real_api_key, real_api_secret)

def buy_stock_market_order(symbols):
    ## Gather available cash
    account_data = exchange.get_account_info()
    cash = int(account_data['cash'].split('.')[0])
    ## Divide total cash by number of stocks to buy to get allotted cash for each stock.
    cash_allotted_per_stock = int(cash / len(symbols))
    for sym in symbols:
        ## Get current bid for stock
        try:
            price = exchange.get_latest_stock_bar(sym)['bar']['c']
            if price > cash_allotted_per_stock:
                resp =  exchange.buy_order_market(sym, '1') ## if share price exceeds allotted cash for each stock in list buy 1 share.
            else:
                shares = str(int(cash_allotted_per_stock / price))
                resp = exchange.buy_order_market(sym, shares)
        except ZeroDivisionError as e:
            print(f'Error: {e}')

def analyze_positions():
    ## analyze open positions and close based on p/l.
    positions = exchange.get_open_positions()
    for position in positions:
        symbol = position['symbol']
        pnl_pct = position['unrealized_plpc']
        excluded_zeros = ('0.0000', '-0.0000')
        if pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) < -0.03:
           exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 1.00:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.95:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.90:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.85:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.80:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.75:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.70:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.65:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.60:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.55:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.50:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.45:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.40:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.35:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.30:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.25:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.20:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.16:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.12:
            exchange.close_single_position(symbol)
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.08:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.07:
            exchange.close_single_position(symbol)
        else:
            continue

def close_all_positions():
    for position in exchange.get_open_positions():
        if position['asset_class'] == 'us_equity':
            exchange.close_single_position(position['symbol'])
            sleep(1)
        else:
            continue

def account_balance():
    equity = exchange.get_account_info()['equity']
    cash = exchange.get_account_info()['cash']
    now = datetime.now()
    positions = str(len(exchange.get_open_positions()))
    print(f'\n\n|| Current Account Balance as of {now} ||')
    print(f'equity: {equity}')
    print(f'cash: {cash}')
    print(f'positions: {positions}')
    return cash

def get_stock_rsi(symbols:list):
    #### Get Relative Strength Index for 14 days
    all_symbols_rsi = {}
    today_raw = datetime.now()
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = (today_raw - timedelta(days=25)).strftime('%Y-%m-%d')
    end_time = today
    timeframe = '1Day'
    for sym in symbols: ### iterate through symbols and gather RSI
        bars = exchange.get_historical_stock_bars(sym, timeframe, start_time, end_time)
        gains = []
        losses = []
        for bar in range(0, 13): ### exclude today in iteration, and only get 14 day RSI
            current_cp = bars['bars'][bar]['c'] ### close price for current day's in loop
            prev_cp = bars['bars'][bar+1]['c'] ### close price for previous day's in loop
            diff = float(current_cp - prev_cp)
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                losses.append(abs(diff)) ## losses expressed as positive values
                gains.append(0)
        try:
            avg_gain = sum(gains) / 14
        except ZeroDivisionError:
            avg_gain = 1
        try:
            avg_loss = sum(losses) / 14
        except ZeroDivisionError:
            avg_loss = 1
        try:
            RS = avg_gain / avg_loss ## Relative Strength
        except:
            if avg_gain != 0 and avg_loss == 0:
                RS = 100
            elif avg_gain == 0 and avg_loss != 0:
                RS = 0
        RSI = 100 - (100 / (1 + RS)) ## Relative Strength Index
        print(RSI)

def get_most_active_stocks(num_stocks, price_limit):
 #### Get Most Active Stocks ####
 #### Limit number of stocks and specify stock price limit to trade
    symbols = []
    most_active = exchange.get_most_active_stocks_by_volume(num_stocks)['most_actives'] ## specify top returned. 100 max
    for sym in most_active:
        price = exchange.get_latest_stock_bar(sym['symbol'])['bar']['c']
        vwap = exchange.get_latest_stock_bar(sym['symbol'])['bar']['vw']
        if int(float(price)) <= price_limit and price > vwap: ## limit to stocks under a specified price point and with price > vwap
            symbols.append(sym['symbol'])
    return symbols
    
if __name__ == '__main__':
    print()
    print('$'*75)
    print('\nEgga\'s stock trading bot is now running.')
    print('Author: eggadigga\n')
    print('$'*75)

# #### Open New Positions after 1:30PM ET. Randomize symbols returned in list
#     symbols = get_most_active_stocks(num_stocks=100, price_limit=80)
#     cash = account_balance()
#     print('\nOpening new positions with available funds in just a minute...\n')
#     sleep(65) ## wait a little over a minute to avoid hitting rate limit

# #### Wait for market to close before returning to beginning
#     while exchange.get_market_clock()['is_open'] == True:
#         account_balance()
#         sleep(60)
#     print('\ngood night')
    
    symbie = ['nvda']
    get_stock_rsi(symbie)