class AlphaVantage():
    def __init__(self, apikey):
        '''
        AlphaVantage market data class.
        '''
        from requests import Session
        self.apikey = apikey
        self.baseurl = 'https://www.alphavantage.co/query'
        self.commonheader = {'content-type': 'application/json'}
        self.session = Session()

    def get_stock_quote(self, symbol):
        '''
        Return latest stock quote and volume.
        :param symbol => Stock ticker.
        '''
        parameters = {
            'apikey': self.apikey, 
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        resp = self.session.get(self.baseurl, headers=self.commonheader, params=parameters, verify=True).json()
        return resp

    def get_time_series_daily(self, symbol):
        '''
        Return time series daily data.
        :param symbol => Stock ticker.
        '''
        parameters = {
            'apikey': self.apikey, 
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol
        }
        resp = self.session.get(self.baseurl, headers=self.commonheader, params=parameters, verify=True).json()
        return resp
    
    def get_top_20_gla(self):
        '''
        Return top 20 gainers, losers, and most active traded.
        '''
        parameters = {
            'apikey': self.apikey, 
            'function': 'TOP_GAINERS_LOSERS',
        }
        resp = self.session.get(self.baseurl, headers=self.commonheader, params=parameters, verify=True).json()
        return resp
