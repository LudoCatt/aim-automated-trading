import pandas as pd
import numpy as np
from auto_trading_aim.portfolio import Portfolio

class PortfolioBuilder(object):
    def __init__(self, capital, data, min_invest):
        self.capital=capital
        self.data=data
        self.min_invest=min_invest
        self.prezzi={}
        self.rendimenti={}
        self.e=np.empty((0,1))
        self.keys_in_order = data.dict.keys()
        for tick in self.keys_in_order:
            self.prezzi[tick]=data.dict[tick].prices
            self.rendimenti[tick]=self.prezzi[tick].pct_change(1)
            self.rendimenti[tick]=self.rendimenti[tick][self.rendimenti[tick].notna()]
            np.append(self.e, self.rendimenti[tick].mean())
        self.rendimenti=pd.DataFrame.from_dict(self.rendimenti)
        self.V=np.array(self.rendimenti.cov())
        self.size=np.shape(self.V)[0]

    def min_var(self):
        V_1 = np.linalg.inv(self.V)
        uno = np.ones(self.size, 1)
        num=np.dot(V_1,uno)
        den=np.dot(np.transpose(uno),num)
        w=(num/den)*self.min_invest*self.capital # per minimizzare la varianza si investe il meno possibile
        allocation={}
        i=0
        for tick in list(self.rendimenti.columns):
            allocation[tick]=int(np.around(w[i]/self.prezzi[tick][0])) # mi dicono dalla regia che non si possono comprare frazioni di azioni
            i=i+1
        ww=np.dot(self.V,w)
        ww=np.dot(np.transpose(w),ww)
        print(ww)
        return Portfolio(allocation, self.prezzi)

    def rate_mean_std(self):
# Con simulazione casuale di portafogli
# non importa quanto investiamo ma la frazione per quanto riguarda il rapporto
        n_iter=4000
        best_w=np.empty((0,1))
        np.random.seed(1)
        for i in range(n_iter):
            random_w=np.random.rand(self.size, 1)*2-1



