class AlpacaReal():
    def __init__(self, api_key, api_secret):
        '''
        Alpaca API instance for Real Trading
        :param api_key => Alpaca Real API Key
        :param api_secret => Alpaca Real API Secret
        '''
        from requests import Session
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = Session()
        self.common_headers = {
            'content-type': 'application/json',
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.api_secret
        }
        self.base_uri = 'https://api.alpaca.markets'
        
    def get_account_info(self):
        '''
        Returns current Alpaca account information (i.e. buying power, balance, account status, etc.)
        '''
        uri = self.base_uri + '/v2/account'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def get_watchlist(self):
        '''
        Returns Alpaca account watchlist.
        '''
        uri = self.base_uri + '/v2/watchlists'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def get_market_clock(self):
        '''
        Returns Market Clock.
        '''
        uri = self.base_uri + '/v2/clock'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def get_assets(self):
        '''
        Returns all Alpaca tradeable assets.
        '''
        uri = self.base_uri + '/v2/assets'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def get_crypto_assets(self):
        '''
        Returns all Alpaca tradeable crypto assets.
        '''
        uri = self.base_uri + '/v2/assets'
        params = {
            'status': 'active',
            'asset_class': 'crypto'
        }
        return self.session.get(uri, headers=self.common_headers, params=params, verify=True).json()
    
    def get_single_asset(self, symbol):
        '''
        Returns Single Asset.
        :param symbol => Stock Symbol (uppercase)
        '''
        uri = self.base_uri + f'/v2/assets/{symbol.upper()}'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def buy_order_trail_stop(self, symbol, shares:str, trail_percentage:str):
        '''
        Places Alpaca buy order with trailing stop percentage.
        :params symbol => Stock ticker symbol.
        :params shares => Quantity of shares.
        :params percent => Trailing percent (needs to be > 0.1).
        '''
        uri = self.base_uri + f'/v2/orders'
        parameters = {
            'symbol': symbol.upper(),
            'side': 'buy',
            'qty': shares,
            'type': 'trailing_stop',
            'trail_percent': trail_percentage,
            'extended_hours': False,
            'time_in_force': 'day'
            }
        return self.session.post(uri, headers=self.common_headers, json=parameters, verify=True).json()
    
    def buy_order_limit(self, symbol, shares:str, limit:str):
        '''
        Places Alpaca buy limit order.
        :params symbol => Stock ticker symbol.
        :params shares => Quantity of shares.
        :params limit => Price limit.
        '''
        uri = self.base_uri + f'/v2/orders'
        parameters = {
            'symbol': symbol.upper(),
            'side': 'buy',
            'qty': shares,
            'type': 'limit',
            'limit_price': limit,
            'extended_hours': False,
            'time_in_force': 'day'
            }
        return self.session.post(uri, headers=self.common_headers, json=parameters, verify=True).json()
    
    def buy_order_market(self, symbol, shares:str):
        '''
        Places Alpaca buy market order.
        :params symbol => Stock ticker symbol.
        :params shares => Quantity of shares.
        '''
        uri = self.base_uri + f'/v2/orders'
        parameters = {
            'symbol': symbol.upper(),
            'side': 'buy',
            'qty': shares,
            'type': 'market',
            'extended_hours': False,
            'time_in_force': 'day'
            }
        return self.session.post(uri, headers=self.common_headers, json=parameters, verify=True).json()
    
    def buy_crypto_order_market(self, symbol, amount:str):
        '''
        Places Alpaca buy market order.
        :params symbol => Crypto ticker symbol.
        :params shares => Quantity of shares.
        '''
        uri = self.base_uri + f'/v2/orders'
        parameters = {
            'symbol': symbol.upper(),
            'side': 'buy',
            'notional': amount,
            'type': 'market',
            'time_in_force': 'gtc'
            }
        return self.session.post(uri, headers=self.common_headers, json=parameters, verify=True).json()
    
    def get_order_list(self):
        '''
        Return list of orders.
        '''
        uri = self.base_uri + f'/v2/orders'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def cancel_order_list(self):
        '''
        Cancel all orders.
        '''
        uri = self.base_uri + f'/v2/orders'
        return self.session.delete(uri, headers=self.common_headers, verify=True).json()
    
    def get_open_positions(self):
        '''
        Return open positions.
        '''
        uri = self.base_uri + f'/v2/positions'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def close_all_positions(self):
        '''
        Closes all open positions.
        '''
        uri = self.base_uri + f'/v2/positions'
        parameters = {
            'cancel_orders': True
            }
        return self.session.delete(uri, headers=self.common_headers, json=parameters, verify=True).json()
    
    def close_single_position(self, symbol):
        '''
        Close single position.
        '''
        uri = self.base_uri + f'/v2/positions/{symbol}'
        parameters = {
            'percentage': 100
            }
        return self.session.delete(uri, headers=self.common_headers, json=parameters, verify=True).json()

    def get_latest_stock_quote(self, symbol):
        '''
        Return latest stock quote.
        :param symbol => Stock symbol.
        '''
        uri = f'https://data.alpaca.markets/v2/stocks/{symbol.upper()}/quotes/latest'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def get_latest_stock_bar(self, symbol):
        '''
        Return latest stock bar.
        :param symbol => Stock symbol.
        '''
        uri = f'https://data.alpaca.markets/v2/stocks/{symbol.upper()}/bars/latest'
        params = {'feed': 'iex'}
        return self.session.get(uri, headers=self.common_headers, params=params, verify=True).json()

    def get_latest_crypto_quote(self, symbol, real_apikey, real_apisecret):
        '''
        Return latest crypto quote. Shared between paper and live trading environments, hence passing real keys/secret.
        :param symbol => Crypto symbol.
        '''
        uri = f'https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes'
        headers = {
            'content-type': 'application/json',
            'APCA-API-KEY-ID': real_apikey,
            'APCA-API-SECRET-KEY': real_apisecret
        }
        params = {'symbols': symbol}
        return self.session.get(uri, headers=headers, params=params, verify=True).json()
    
    def get_most_active_stocks_by_volume(self, top:int):
        '''
        Get most active stocks by volume.
        :param top => qty to return. Max is 100
        '''
        uri = 'https://data.alpaca.markets/v1beta1/screener/stocks/most-actives'
        params = {
            'by': 'volume',
            'top': str(top)
        }
        return self.session.get(uri, headers=self.common_headers, params=params, verify=True).json()
    
    def get_most_active_stocks_by_trades(self, top:int):
        '''
        Get most active stocks by trades.
        :param top => qty to return. Max is 100
        '''
        uri = 'https://data.alpaca.markets/v1beta1/screener/stocks/most-actives'
        params = {
            'by': 'trades',
            'top': top
        }
        return self.session.get(uri, headers=self.common_headers, params=params, verify=True).json()
    
    def get_top_market_movers(self, top:int):
        '''
        Get top market movers.
        :param top => qty to return. Max is 50
        '''
        uri = 'https://data.alpaca.markets/v1beta1/screener/stocks/movers'
        params = {
            'top': str(top)
        }
        return self.session.get(uri, headers=self.common_headers, params=params, verify=True).json()