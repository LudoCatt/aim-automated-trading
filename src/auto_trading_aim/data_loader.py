import yfinance as yf
import matplotlib.pyplot as plt

class DataLoader(object):

    def __init__(self, ticker, start, end, interval):
        yftk = yf.Ticker(ticker) 
        self.history=yftk.history(start=start, end=end, interval=interval)
        self.prices=self.history.loc[:,'Close']
        self.volumes=self.history.loc[:,'Volume']
        self.ticker=ticker
        self.start=start
        self.end=end
        self.interval=interval
        self.__calcolo() # alla prima chiamata salvo tutti i dati richiesti per la stampa

    def __calcolo(self):
        self.mC=self.prices.min()
        self.mV=self.volumes.min()
        self.MC=self.prices.max()
        self.MV=self.volumes.min()
        self.meC=self.prices.mean()
        self.meV=self.volumes.mean()
        self.fC=self.prices[0]
        self.lC=self.prices[-1]
        self.fV=self.volumes[0]
        self.lV=self.volumes[-1]

    def __repr__(self):
        return '{} data from {} to {}, {}\n\
Close -> min: {} max: {} mean: {}\n\
 first day: {} last day: {}\n\
Volume -> min: {} max: {} mean: {}\n\
 first day: {} last day: {}\n'\
                 .format(self.ticker, self.start, self.end, self.interval, self.mC, self.MC, self.meC, \
                     self.fC, self.lC, self.mV, self.MV, self.meV, self.fV, self.lV)

    def plot(self, tipo):
        if tipo == 'Prices':
            Tipo='Close'
        elif tipo == 'Volumes':
            Tipo='Volume'
        else:
            raise NameError
        self.history.plot(y=Tipo, use_index=True)
        plt.title('{} of {}'.format(tipo, self.ticker), fontdict=None, loc='center', pad=None)
        plt.show()