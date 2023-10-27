#! python3

'''
name: paper_crypto_trader_egg.py
description: trade bot placing random crypto trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_paper import AlpacaPaper
from modules.av_market_data import AlphaVantage
from pprint import pformat
import os, sys, random
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

def buy_crypto_market_order(symbols):
    ## Gather available cash
    account_data = exchange.get_account_info()
    cash = int(account_data['cash'].split('.')[0])
    ## Divide total cash by number of crypto to buy to get allotted cash for each.
    cash_allotted_per_crypto = int(cash / len(symbols))
    for sym in symbols:
        ## submit market buy order. Pop out Symbols from list of failed order
        try:
            resp = exchange.buy_crypto_order_market(sym, cash_allotted_per_crypto)
            if 'code' in resp:
                if resp['code'] == 40310000:
                    symbols.remove(sym) ## pop out crypto symbol with failed transaction
        except ZeroDivisionError as e:
            print(f'Error: {e}')

    ## submit another market buy order for crypto we can buy.
    cash = int(account_data['cash'].split('.')[0])
    cash_allotted_per_crypto = int(cash / len(symbols))
    for sym in symbols:
        try:
            resp = exchange.buy_crypto_order_market(sym, cash_allotted_per_crypto)
        except ZeroDivisionError as e:
            print(f'Error: {e}')

def analyze_crypto_positions():
    ## analyze open positions and close based on p/l.
    positions = exchange.get_open_positions()
    for position in positions:
        symbol = position['symbol']
        pnl_pct = position['unrealized_plpc']
        if pnl_pct.startswith(('0.0000', '-0.0000')) == False and position['asset_class'] == 'crypto' and float(pnl_pct) < -0.02:
           exchange.close_single_position(symbol)
        elif pnl_pct.startswith(('0.0000', '-0.0000')) == False and position['asset_class'] == 'crypto' and float(pnl_pct) > 0.07:
            exchange.close_single_position(symbol)
        else:
            continue

def check_open_positions():
    open_crypto_positions = []
    for cp in exchange.get_open_positions():
        if cp['asset_class'] == 'crypto':
            open_crypto_positions.append(cp['symbol'])
    return len(open_crypto_positions)

def account_balance():
    equity = exchange.get_account_info()['equity']
    cash = exchange.get_account_info()['cash']
    now = datetime.now()
    print(f'\n\n|| Current Account Balance as of {now} ||')
    print(f'equity: {equity}')
    print(f'cash: {cash}')

if __name__ == '__main__':
    print()
    print('$'*75)
    print('\nEgga\'s crypto trading bot is now running.')
    print('Author: eggadigga\n')
    print('$'*75)

    while True:
    ### Gather available crypto tradeable assets in Alpaca
        crypto_symbols = []
        for asset in exchange.get_crypto_assets():
            crypto_symbols.append(asset['symbol'])

    ### Buy crypto market order, shuffle list of symbols
        print("Opening crypto positions...")
        buy_crypto_market_order(random.sample(crypto_symbols, len(crypto_symbols)))

    ### Loop through positions for 3 hours. Close based on p/l percentages.
    ### Loop breaks after 3 hours to then close all positions and restart cycle.
        current_time = datetime.now()
        close_all_positions_time = current_time + timedelta(hours=1)
        while current_time < close_all_positions_time:
            analyze_crypto_positions()
            current_time = datetime.now()
            account_balance()
            ### break loop if all positions are closed
            if check_open_positions == 0:
                break
            sleep(120)
        for position in exchange.get_open_positions():
            if position['asset_class'] == 'crypto':
                exchange.close_single_position(position['symbol'])
                sleep(1)
            else:
                continue
        print('\nCrypto positions closed...')

