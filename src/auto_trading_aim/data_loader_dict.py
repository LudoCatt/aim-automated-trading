from email import header
from auto_trading_aim.data_loader import DataLoader
from auto_trading_aim.portfolio import Portfolio

class DataLoaderDict(object):

    def __init__(self, tickers, start, end, interval):
        self.dict={}
        for tick in tickers:
            self.dict[tick]=DataLoader(tick, start, end, interval)

    def save(self, path):
        f=open(path, 'w')
        for tick in self.dict.values():
            print(tick.ticker, file=f)
            print(tick.history.to_string(header=True, index=True), file=f)
            print('',file=f)
        f.close()

    def __getitem__(self, tick):
        return self.dict[tick]

    def build_portfolio(self, allocation):
        prices_dict={}
        for tick in allocation.keys():
            prices_dict[tick]=self.dict[tick].prices
        return Portfolio(allocation, prices_dict)