#! python3

'''
name: roboegg.py
description: trade bot placing random trades on egga's dime
author: eggadigga
'''

from dotenv import load_dotenv
from configparser import ConfigParser
from modules.alpaca_paper import AlpacaPaper
from pprint import pformat
import os, sys

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
api_key = os.environ['apcapaperkey']
api_secret = os.environ['apcapapersecret']
exchange = AlpacaPaper(api_key, api_secret)

## Gather Alpaca Account info
account_data = exchange.get_account_info()
print(pformat(account_data))

## Get Alpaca watchlists
# watchlist = exchange.get_watchlist()
# print(pformat(watchlist))

## Get Market Clock
# market_clock = exchange.get_market_clock()
# # print(pformat(market_clock))

## Get asset data from stock symbols in text file
def get_stock_ticker_info():
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

def buy_stock_market_order(shares):
    for sym in symbol_list:
        resp = exchange.buy_order_market(sym, shares)

if __name__ == '__main__':
    # buy_stock_trail_stop_order('10', '0.1')
    # buy_stock_limit_order('10', '6')
    buy_stock_market_order('10')
    orders = exchange.get_order_list()
    for order in orders:
        print(order['created_at'])
        print(order['symbol'])
        print(order['order_type'])
        print()