'''
Created on 28 Dec 2017

@author: yev
'''

import datetime as dt

from pyfbox.backtesting import BacktestingService as service


if __name__ == '__main__':
    backtester = service.Backtester("AAPL",dt.datetime(2014, 1, 1),dt.datetime(2014, 12, 31))
    backtester.start_backtest()

    import matplotlib.pyplot as plt
    backtester.rpnl.plot()
    plt.show()

    backtester.upnl.plot()
    plt.show()