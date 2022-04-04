import yfinance as yf
import numpy as np
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
        close=np.array(self.prices)
        volume=np.array(self.volumes)
        self.mC=np.min(close)
        self.mV=np.min(volume)
        self.MC=np.max(close)
        self.MV=np.max(volume)
        self.meC=np.mean(close)
        self.meV=np.mean(volume)
        self.fC=close[0]
        self.lC=close[-1]
        self.fV=volume[0]
        self.lV=volume[-1]

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