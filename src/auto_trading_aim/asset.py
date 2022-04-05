import matplotlib.pyplot as plt
import auto_trading_aim.portfolio as ptf

class Asset(object):
    def __init__(self, ticker_name, prices, volume_owned):
        self.ticker_name = ticker_name
        self.prices = prices
        self.mkt_returns=self.prices.pct_change(1)
        self.mkt_returns=self.mkt_returns[self.mkt_returns.notna()]
# per il primo non è definito il rendimento, si potrebbero in alternativa selezionare solo i
# valori ben definiti con notna
        self.volume_owned = volume_owned
        self.__calcolo()

    def __calcolo(self):
        self.mu=self.mkt_returns.mean()
        self.ss=self.mkt_returns.var()

    def __repr__(self):
        return '{} #{} | mu: {} | sigma_squared: {}\n'.format(self.ticker_name, self.volume_owned, self.mu, self.ss)

    def hist(self):
        plt.hist(self.mkt_returns, bins=len(list(self.mkt_returns))//10, density=True, rwidth=0.9)
        plt.title('Rendimenti di {}'.format(self.ticker_name))
        plt.xlabel('Rendimenti')
        plt.ylabel('Frequenza')
        plt.show()

    def __truediv__(self, n):
        new_volume = self.volume_owned//n
        return Asset(self.ticker_name, self.prices, new_volume)

    def __add__(self, oggetto2):
        portafoglio=ptf.Portfolio({}, {})
        if self.ticker_name == oggetto2.ticker_name:
            portafoglio[self.ticker_name] = Asset(self.ticker_name, self.prices, self.volume_owned+oggetto2.volume_owned)
        else:
            portafoglio[self.ticker_name] = Asset(self.ticker_name, self.prices, self.volume_owned)
            portafoglio[oggetto2.ticker_name] = Asset(oggetto2.ticker_name, oggetto2.prices, oggetto2.volume_owned)
        return portafoglio
            
    