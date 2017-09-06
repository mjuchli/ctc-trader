#%cd code/lstm-prototype
import peewee as pw
import models as m
import neural_network as nn
import numpy as np
import data as d
import validation as v
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import time
from multiprocessing import Process
from candle_processor import *
from executor import *
from sklearn.model_selection import train_test_split
import strategy

class CandleStream:
    def __init__(self, candleClass, limit = 0):
        self.candleClass = candleClass
        self.limit = limit
        self.size = 15

    def getSize(self):
        return self.size

    def get(self):
        return (self.candleClass.select().order_by(self.candleClass.id.desc()).limit(self.limit))[::-1]


class Trader:
    def __init__(self, stream, executor, strategy):
        self.stream = stream
        self.executor = executor
        self.strategy = strategy
        self.candleSize = self.stream.getSize() # number of accumulated 1-minute candles
        self.retrainWait = 5 # minutes (e.g. candles) to wait until model retrain
        self.LB = 10

    def plot_graph(self, Ytrain, Ytest, Ypredict):
        plt.clf()
        if Ytrain:
            offset = [None for x in range(len(Ytrain))]
            plt.plot(Ytrain)
            plt.plot(np.array(offset+Ytest))
            plt.plot(np.array(offset+Ypredict.tolist()), color="red")
        else:
            plt.plot(Ytest)
            plt.plot(Ypredict, color="red")
        plt.show()
        #plt.pause(10)

    def backtest(self, plot = False):
        data = self.stream.get()
        cp = CandleProcessor(data, self.candleSize, self.LB)
        X, Y, scalerX, scalerY = cp.get_data_set(scaled = True)
        X_train, X_test, y_train, y_test = cp.non_shuffling_train_test_split(X, Y, test_size=0.01)
        mdl = nn.createModelStandard(X_train, y_train, epochs = 20, batch_size = 200)
        pred = scalerY.inverse_transform(mdl.predict(X_test)).flatten()
        y_test = scalerY.inverse_transform(y_test).tolist()
        y_train = scalerY.inverse_transform(y_train).tolist()

        if plot:
            self.plot_graph(y_train, y_test, pred)

        for i in range(0, len(pred)-1):
            self.strategy.decide(y_test[i], pred[i], verbose=False)
        self.strategy.closeCrypto(y_test[-1])

    def train(self, cp):
        X, Y, scalerX, scalerY = cp.get_data_set(scaled = True)
        lastKnown = (cp.get_feature_set())[-1]
        print "Train on: " + str(X.shape)
        mdl = nn.createModelStandard(X, Y, epochs = 20, batch_size = 200)
        return mdl, scalerX, scalerY, lastKnown, X, Y

    def run(self):
        data = self.stream.get()
        cp = CandleProcessor(data, self.candleSize, self.LB)
        mdl, scalerX, scalerY, lastKnown, X, Y = self.train(cp)
        print "Train until candle: " + str(lastKnown)

        #plot
        # X_unlabelled, Y_unlabelled, _, _ = cp.get_data_set_unlablled(scaled=True)
        # predict = scalerY.inverse_transform(mdl.predict(X_unlabelled)).flatten().tolist()
        #Ytrain = (np.squeeze(scalerY.inverse_transform(Y))).tolist()
        #Ypredict = [None for x in range(len(Ytrain))] + predict
        #self.plot_graph(None, Ytrain, Ypredict)

        retrainCount = 0
        lastKnown = []
        while True:
            new_data = self.stream.get()
            cp_new = CandleProcessor(new_data, self.candleSize, self.LB)
            lastCandle = (cp_new.get_feature_set())[-1]
            if set(lastKnown) == set(lastCandle):
                print "Candle not updated yet"
            else:
                print "New candle: " + str(lastCandle)
                lastKnownPrice = lastCandle[0]
                lastX, lastY, _, _ = cp.get_data_set_unlablled(scaled=True)
                predict = scalerY.inverse_transform(mdl.predict(lastX)).flatten().tolist()
                print "Prediction next price: " + str(predict[-1])

                self.strategy.decide(lastKnownPrice, predict[-1], verbose=True)

                retrainCount = retrainCount + 1
                if retrainCount >= self.retrainWait:
                    retrainCount = 0
                    data = self.stream.get()
                    cp = CandleProcessor(data, self.candleSize, self.LB)
                    mdl, scalerX, scalerY, lastKnown, X, Y = self.train(cp)
                    print "Train until candle: " + str(lastKnown)

            lastKnown = lastCandle
            time.sleep(10)

cs = CandleStream(m.GdaxCandle, 1000)
e = ExecutorMock(crypto=0.0, fiat=1000.0, market="BTC/USD")
r = Reporter("trades.tsv")
r.setup(crypto=0.0, fiat=1000.0)
e.setReporter(r)
s = strategy.Strategy(executor=e)

trader = Trader(cs, e, s)
#trader.backtest(plot = False)
trader.run()
print r.getTrades()
print e.getAccountBalance()
