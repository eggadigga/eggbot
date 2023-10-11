from requests import Session

class AlpacaPaper():
    def __init__(self, api_key, api_secret):
        '''
        Alpaca API instance for Paper Trading
        :param api_key => Alpaca Paper API Key
        :param api_secret => Alpaca Paper API Secret
        '''
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = Session()
        self.common_headers = {
            'content-type': 'application/json',
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.api_secret
        }
        self.base_uri = 'https://paper-api.alpaca.markets'
        
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
    
    def get_single_asset(self, symbol):
        '''
        Returns Single Asset.
        :param symbol => Stock Symbol (uppercase)
        '''
        uri = self.base_uri + f'/v2/assets/{symbol.upper()}'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
    
    def buy_order_trail_stop(self, symbol, amount:str, trail_percent:str):
        '''
        Places Alpaca buy order with trailing stop percentage.
        :params symbol => Stock ticker symbol.
        :params amount => Dollar amount for trade.
        :params percent => Trailing percent. 
        '''
        uri = self.base_uri + f'/v2/orders'
        headers = {
            'symbol': symbol,
            'notional': amount,
            'side': 'buy',
            'type': 'trailing_stop',
            'trail_percent': trail_percent,
            'content-type': 'application/json',
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.api_secret,
        }
        return self.session.post(uri, headers=headers, verify=True).json()
    
    def get_order_list(self):
        uri = self.base_uri + f'/v2/orders'
        return self.session.get(uri, headers=self.common_headers, verify=True).json()
