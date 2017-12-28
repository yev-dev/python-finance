'''
Created on 28 Dec 2017

@author: yev
'''

import pandas as pd

from pyfbox.backtesting import Order as o

""" Base strategy for implementation """
class Strategy:
    def __init__(self):
        self.event_sendorder = None

    def event_tick(self, market_data):
        pass

    def event_order(self, order):
        pass

    def event_position(self, positions):
        pass

    def send_market_order(self, symbol, qty, is_buy, timestamp):
        if not self.event_sendorder is None:
            order = o.Order(timestamp, symbol, qty, is_buy, True)
            self.event_sendorder(order)
            

"""
Implementation of a mean-reverting strategy
based on the Strategy class
"""
class MeanRevertingStrategy(Strategy):
    def __init__(self, symbol,
                 lookback_intervals=20,
                 buy_threshold=-1.5,
                 sell_threshold=1.5):
        Strategy.__init__(self)
        self.symbol = symbol
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.prices = pd.DataFrame()
        self.is_long, self.is_short = False, False

    def event_position(self, positions):
        if self.symbol in positions:
            position = positions[self.symbol]
            self.is_long = True if position.net > 0 else False
            self.is_short = True if position.net < 0 else False

    def event_tick(self, market_data):
        self.store_prices(market_data)

        if len(self.prices) < self.lookback_intervals:
            return

        signal_value = self.calculate_z_score()
        timestamp = market_data.get_timestamp(self.symbol)

        if signal_value < self.buy_threshold:
            self.on_buy_signal(timestamp)
        elif signal_value > self.sell_threshold:
            self.on_sell_signal(timestamp)

    def store_prices(self, market_data):
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, "close"] = \
            market_data.get_last_price(self.symbol)
        self.prices.loc[timestamp, "open"] = \
            market_data.get_open_price(self.symbol)

    def calculate_z_score(self):
        self.prices = self.prices[-self.lookback_intervals:]
        returns = self.prices["close"].pct_change().dropna()
        z_score = ((returns-returns.mean())/returns.std())[-1]
        return z_score

    def on_buy_signal(self, timestamp):
        if not self.is_long:
            self.send_market_order(self.symbol, 100,
                                   True, timestamp)

    def on_sell_signal(self, timestamp):
        if not self.is_short:
            self.send_market_order(self.symbol, 100,
                                   False, timestamp)

