import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

class DataLoader(object):

    def __init__(self, ticker, start, end, interval):
        yftk = yf.Ticker(ticker) 
        self.history=yftk.history(start=start, end=end, interval=interval)
        self.ticker=ticker
        self.start=start
        self.end=end
        self.interval=interval
        self.calcolo() # alla prima chiamata salvo tutti i dati richiesti per la stampa

    def calcolo(self):
        self.close=np.array(self.history.loc[:,'Close'])
        self.volume=np.array(self.history.loc[:,'Volume'])
        self.mC=np.min(self.close)
        self.mV=np.min(self.volume)
        self.MC=np.max(self.close)
        self.MV=np.max(self.volume)
        self.meC=np.mean(self.close)
        self.meV=np.mean(self.volume)
        self.fC=self.close[0]
        self.lC=self.close[-1]
        self.fV=self.volume[0]
        self.lV=self.volume[-1]

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
        plt.title(tipo, fontdict=None, loc='center', pad=None)
        plt.show()

