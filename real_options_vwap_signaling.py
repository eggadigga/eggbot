#! python3

'''
name: real_options_vwap_signaling.py
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

## Alpaca Instance Setup
real_api_key = os.environ['apcarealkey']
real_api_secret = os.environ['apcarealsecret']
exchange = AlpacaReal(real_api_key, real_api_secret)

def get_most_active_stocks(num_stocks, price_limit, type_):
 #### Get Most Active Stocks ####
 #### Limit number of stocks and specify stock price limit to trade
    '''
    :param type_ => call or put
    '''
    symbols = []
    most_active = exchange.get_most_active_stocks_by_volume(num_stocks)['most_actives'] ## specify top returned. 100 max
    for sym in most_active:
        price = exchange.get_latest_stock_bar(sym['symbol'])['bar']['c']
        vwap = exchange.get_latest_stock_bar(sym['symbol'])['bar']['vw']
        if type_ == 'call':
            if int(float(price)) <= price_limit and price > vwap: ## use for call
                symbols.append(sym['symbol'])
        else:
            if int(float(price)) <= price_limit and price < vwap: ## use for put
                symbols.append(sym['symbol'])
    return symbols
    
if __name__ == '__main__':
    print()
    print('$'*75)
    print('\nEgga\'s stock trading bot is now running.')
    print('Author: eggadigga\n')
    print('$'*75)

    if len(sys.argv) != 2:
        raise Exception('Error: Missing argument "call" or "put"!!')
    elif sys.argv[1] not in ['call', 'put']:
        raise Exception('Error: Invalid argument. Accepted are "call" or "put" only!')
    else:
        option = sys.argv[1]
    symbols = get_most_active_stocks(num_stocks=100, price_limit=400,type_=option)
    print(symbols)