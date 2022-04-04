import pandas as pd
import matplotlib.pyplot as plt
from auto_trading_aim.asset import Asset
import numpy as np

class Portfolio(object):
    def __init__(self, allocation, prices_dict):
        self.allocation=allocation
        self.prices_dict=prices_dict # so di sprecare memoria inutilmente ma è comodo per add
        self.dict={}
        for tick in allocation.keys():
            self.dict[tick]=Asset(tick, prices_dict[tick], allocation[tick])

    def __getitem__(self, ticker):
        return self.dict[ticker]

    def __setitem__(self, ticker, asset):
        self.dict[ticker] = asset

    def __repr__(self):
        stringa={}
        for tick in self.dict.keys():
            mu=np.mean(np.array(self.dict[tick].mkt_returns))
            ss=np.var(np.array(self.dict[tick].mkt_returns))
            stringa[tick]='{} #{} | mu: {} | sigma_squared: {}'.format(tick, self.dict[tick].volume_owned, mu, ss)
        return str(stringa)

    def hist(self):
        self.__calcola_valori()
        plt.hist(self.mkt_returns, bins=len(list(self.mkt_returns))//10, density=True, rwidth=0.9)
        plt.title('Rendimenti del portafoglio')
        plt.xlabel('Rendimenti')
        plt.ylabel('Frequenza')
        plt.show()

    def plot(self):
        self.__calcola_valori()
        plt.plot(self.valore)
        plt.title('Valore del portafoglio nel tempo')
        plt.xlabel('t')
        plt.ylabel('Valore')
        plt.show()

    def __calcola_valori(self):
        ticks=list(self.dict.keys())
        valore=self.dict[ticks[0]].prices
        for tick in ticks[1:]:
            valore=valore + (self.dict[tick].volume_owned*self.dict[tick].prices)
        self.valore=valore
        self.mkt_returns=valore.pct_change(1)[1:]

    def __add__(self, portafoglio2):
        new_allocation={**self.allocation, **portafoglio2.allocation}
        for tick in new_allocation.keys():
            new_allocation[tick]=new_allocation[tick]+self.allocation.get(tick,0)
        new_prices={**self.prices_dict, **portafoglio2.prices_dict}
        return Portfolio(new_allocation, new_prices)

