from cmath import inf
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
            self.e=np.append(self.e, self.rendimenti[tick].mean())
        self.rendimenti=pd.DataFrame.from_dict(self.rendimenti)
        self.V=np.array(self.rendimenti.cov())
        self.size=np.shape(self.V)[0]

    def min_var(self):
        V_1 = np.linalg.inv(self.V)
        uno = np.ones((self.size, 1))
        num = np.dot(V_1,uno)
        den = np.dot(np.transpose(uno),num)
        w = (num/den)*self.min_invest*self.capital # per minimizzare la varianza si investe il meno possibile
        allocation={}
        i=0
        for tick in list(self.rendimenti.columns):
            allocation[tick]=np.around(w[i]/self.prezzi[tick][0]) # mi dicono dalla regia che non si possono comprare frazioni di azioni
            i=i+1
        return Portfolio(allocation, self.prezzi)

    def __calcolo(self):
        V_1 = np.linalg.inv(self.V)
        uno = np.ones((self.size, 1))
        V1=np.dot(V_1,uno)
        Ve=np.dot(V_1,self.e)
        A=np.dot(np.transpose(uno),Ve)
        B=np.dot(np.transpose(self.e),Ve)
        C=np.dot(np.transpose(uno),V1)
        D=np.dot(B,C)-np.dot(A,A)
        res=1/np.sqrt((B*C-A)/(B*D))
# con lunghi e tediosi calcoli questo è il massimo rapporto che si può ottenere 
        print('Massimo rate_mean_std teorico: {}'.format(res))

    def rate_mean_std(self):
        self.__calcolo()
# Con simulazione casuale di portafogli
# non importa quanto investiamo ma la frazione per quanto riguarda il rapporto
# Supponiamo che non ci siano valori troppo estremi e quinsi sia sensato generare w come segue
# Supponiamo anche investa il meno possibile
        n_iter=4000
        best_w=np.empty((0,1))
        np.random.seed(3)
        massimo=-float(inf)
        for i in range(n_iter):
            random_w=np.random.rand(self.size, 1)*2-1
            random_w=random_w/np.sum(random_w) #mi assicuro che la somma sia 1
            media=np.dot(np.transpose(random_w), self.e)
            sigma=np.sqrt(np.dot(np.dot(np.transpose(random_w), self.V),random_w))
            ratio=media/sigma
            if ratio>massimo:
                massimo=ratio
                best_w=random_w
        print('Massimo rate_mean_std ottenuto: {}'.format(massimo))
        best_w = best_w*self.min_invest*self.capital
        allocation={}
        i=0
        for tick in self.keys_in_order:
            allocation[tick]=np.around(best_w[i]/self.prezzi[tick][0])
            i=i+1
        return Portfolio(allocation, self.prezzi)