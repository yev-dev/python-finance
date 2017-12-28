'''
Created on 28 Dec 2017

@author: yev
'''
import pandas_datareader.data as web

""" Store a single unit of data """
class TickData:
    def __init__(self, symbol, timestamp,last_price=0, total_volume=0):
        self.symbol = symbol
        self.timestamp = timestamp
        self.open_price = 0
        self.last_price = last_price
        self.total_volume = total_volume


""" A container to store prices for a symbol """
class MarketData:
    def __init__(self):
        self.__recent_ticks__ = dict()

    def add_last_price(self, time, symbol, price, volume):
        tick_data = TickData(symbol, time, price, volume)
        self.__recent_ticks__[symbol] = tick_data

    def add_open_price(self, time, symbol, price):
        tick_data = self.get_existing_tick_data(symbol, time)
        tick_data.open_price = price

    def get_existing_tick_data(self, symbol, time):
        if not symbol in self.__recent_ticks__:
            tick_data = TickData(symbol, time)
            self.__recent_ticks__[symbol] = tick_data

        return self.__recent_ticks__[symbol]

    def get_last_price(self, symbol):
        return self.__recent_ticks__[symbol].last_price

    def get_open_price(self, symbol):
        return self.__recent_ticks__[symbol].open_price

    def get_timestamp(self, symbol):
        return self.__recent_ticks__[symbol].timestamp

""" Download prices from an external data source """
class MarketDataSource:
    def __init__(self):
        self.event_tick = None
        self.ticker, self.source = None, None
        self.start, self.end = None, None
        self.md = MarketData()

    def start_market_simulation(self):
        data = web.get_data_yahoo(self.ticker, start=self.start, end=self.end);

        for time, row in data.iterrows():
            self.md.add_last_price(time, self.ticker,
                                   row["Close"], row["Volume"])
            self.md.add_open_price(time, self.ticker, row["Open"])

            if not self.event_tick is None:
                self.event_tick(self.md)


