#! python3

'''
name: paper_trader_egg-RSI14-above70_VWAP.py
description: trade bot placing random trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_paper import AlpacaPaper
from pprint import pformat
import os, sys, socket, requests, random
from datetime import datetime, time, timedelta
from time import sleep
from modules.emailTool import sendMail
from argparse import ArgumentParser

## argument parser
parser = ArgumentParser(
    prog='Paper - EGGADIGGA Stock Bot with RSI',
    description='Buy/Sell Stocks',
    epilog='Try not to lose too much money.'
    )

parser.add_argument('price', type=int, help='Price of stock.')
parser.add_argument('price_dir', choices=['<','>'], help='Specify greater than or less than direction of stock price.')
parser.add_argument('rsi', type=int, help='Relative stock index (RSI).')
parser.add_argument('rsi_dir', choices=['<', '>'], type=int, help='Specify greater than or less than direction of RSI measure to determine cost.')
parser.add_argument('-rsi_limit', type=int, help='Specify RSI limit.')
args = parser.parse_args()

sleep(20)
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
real_api_key = os.environ['apcapaperkey']
real_api_secret = os.environ['apcapapersecret']
exchange = AlpacaPaper(real_api_key, real_api_secret)

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
        if pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) < -0.02:
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
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.06:
            continue
        elif pnl_pct.startswith(excluded_zeros) == False and position['asset_class'] == 'us_equity' and float(pnl_pct) > 0.03:
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
    return cash, positions

def get_stock_rsi(symbols:list):
    #### Get Relative Strength Index for 14 days
    overbought_symbols = []
    today_raw = datetime.now()
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = (today_raw - timedelta(days=25)).strftime('%Y-%m-%d')
    end_time = today
    timeframe = '1Day'
    for sym in symbols: ### iterate through symbols and gather RSI
        bars = exchange.get_historical_stock_bars(sym, timeframe, start_time, end_time)
        gains = []
        losses = []
        for bar in range(0, 5): ### exclude today in iteration, and only get 5 day RSI
            try:
                current_cp = bars['bars'][bar]['c'] ### close price for current day's in loop
                prev_cp = bars['bars'][bar+1]['c'] ### close price for previous day's in loop
            except:
                ## Catch failure if symbol doesn't return 14 or more bars. Also continue looping
                print(f'\n{sym} has only {str(len(bars))} bars returned.')
                continue
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
        if RSI > 70 and RSI <= 98:
            overbought_symbols.append(sym)
        gains.clear() ## reset list for next symbol
        losses.clear() ## reset list for next symbol
        sleep(1) ## 1 second sleep for avoiding api rate limit
    return overbought_symbols

def get_most_active_stocks(num_stocks, price_limit):
 #### Get Most Active Stocks ####
 #### Limit number of stocks and specify stock price limit to trade
 #### Get tickers and get mvwap
    symbols = []
    most_active = exchange.get_most_active_stocks_by_volume(num_stocks)['most_actives'] ## specify top returned. 100 max
    for sym in most_active:
        try:
            price = exchange.get_latest_stock_bar(sym['symbol'])['bar']['c']
            if int(float(price)) <= price_limit: ## limit to stocks under a specified price point
                symbols.append(sym['symbol'])
        except Exception as e:
            print(e)
            print(f'Exception occurred in fetching this ticker: "{sym}"')
    sleep(60) ## sleep for a minute before beginning MVWAP analysis
    overbought_symbols = get_stock_rsi(symbols)
    return overbought_symbols

if __name__ == '__main__':
    print()
    print('$'*75)
    print('\nEgga\'s stock trading bot is now running.')
    print('Author: eggadigga\n')
    print('$'*75)

    order_time = time(hour=9, minute=35) ## time open/close position orders are allowed
    script_init_after_market_open = exchange.get_market_clock()['is_open'] ## see if app is run after market open
    market_closed_msg = '\nMarket is currently closed...\n'

    try:
        while True:
        #### Loop until market opens
            day_trade = 'n' ## default value 'n' assumes positions were not opened on current day.
            if exchange.get_market_clock()['is_open'] == False:
                market_is_open = False
            else:
                market_is_open = True
            while market_is_open == False:
                ## Error handle during Alpaca GET request failure during presumed maintenance 
                try:
                    account_balance()
                    print(market_closed_msg)
                    sleep(60)
                    market_is_open = exchange.get_market_clock()['is_open']
                except Exception as e:
                    print(f'\nError: {e}\n')
                    sleep(120)
                    continue
            print('\nMarket is now open... Let the games begin...')
            if script_init_after_market_open == False:
                ### Wait 5 minutes after market open before position analyses
                while datetime.now().time() < order_time:
                    sleep(1)

        #### Gather current time, set sell time to 1:30 PM ET.
        #### While loop analyzing positions throughout day, and sell based on unrealized pnl.
        #### If current time is > 1:30 PM ET, loop breaks and all positions are sold.
        #### If the program is started after market, prompts will occur to close and/or buy positions.
            current_time = datetime.now().time()
            close_all_positions_time = time(hour=13, minute=30)
            if script_init_after_market_open == True:
                script_init_after_market_open = False ## Change to False to avoid hitting this block in subsequent loops
                print('\n!!!!!! Bot initiated during trading hours. Do you want to do any of the following? !!!!!!')
                print('Note: Positions are opened regardless if at least 1 prompt is Yes (Y).')
                prompt = '\nWere new positions opened today? Y or N?\n'
                prompt1 = '\nOpen new positions? Y or N?\n'
                prompt2 = '\nClose all positions? Y or N?\n'
                day_trade = input(prompt).lower()
                while day_trade not in ['y', 'n']:
                    day_trade = input(prompt).lower()
                buy = input(prompt1).lower()
                while buy not in ['y', 'n']:
                    buy = input(prompt1).lower()
                if buy == 'y':
                    day_trade = 'y'
                sell = input(prompt2).lower()
                while sell not in ['y', 'n']:
                    sell = input(prompt2).lower()
                if sell == 'y':
                    close_all_positions()
                    day_trade = 'y'

            if day_trade == 'n':
                while current_time < close_all_positions_time:
                    analyze_positions()
                    current_time = datetime.now().time()
                    cash, positions = account_balance()
                    if positions == '0':
                        break ## break loop if all positions were closed
                    sleep(60)
                close_all_positions()

        #### Open New Positions after 1:30PM ET. If symbols returned. Randomize symbols returned in list
            symbols = get_most_active_stocks(num_stocks=100, price_limit=90)
            cash, positions = account_balance()
            if len(symbols) >= 1:
                print('\nOpening new positions with available funds in just a minute. Purchase randomized for below symbols...\n\n')
                print(* symbols, sep='\n')
                sleep(65) ## wait a little over a minute to avoid hitting rate limit
                buy_stock_market_order(random.sample(symbols, len(symbols)))
                if cash > '10': ## buy more if there's spare 10 dollars or more in spare cash
                    buy_stock_market_order(random.sample(symbols, len(symbols)))
            else:
                print('\n No stocks returned with RSI under 30 and current price below VWAP.\nLet script continue until next day or re-run script at some point today.')

        #### Cancel open orders
            sleep(61)
            exchange.cancel_order_list()

        #### Wait for market to close before returning to beginning
            while exchange.get_market_clock()['is_open'] == True:
                account_balance()
                sleep(60)
    except Exception as e:
        print('\nError: Stock Trading app stopped running')
        print('Reason: ' + str(e))
        app_fail_smtp_alert(e)
        raise(Exception)
        
