import neural_network as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import time
from candle_processor import *
from sklearn.model_selection import train_test_split
from candle_stream import * #remove and reuse class from constructor argument
import sys

class Trader:
    def __init__(self, stream, executor, strategy):
        self.stream = stream
        self.executor = executor
        self.strategy = strategy
        self.candleSize = self.stream.getSize() # number of accumulated 1-minute candles
        self.setup() # DEFAULTS

    def setup(self,
              retrainWait = 5, # minutes (e.g. candles) to wait until model retrain
              decisionWait = 1,
              LB = 5,
              testSize = 0.01,
              epochs = 100,
              batchSize = 200):
        self.retrainWait = retrainWait
        self.decisionWait = decisionWait
        self.LB = LB
        self.testSize = testSize
        self.epochs = epochs
        self.batchSize = batchSize


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
        X_train, X_test, y_train, y_test = cp.non_shuffling_train_test_split(X, Y, test_size=self.testSize)
        mdl = nn.createModelStandard(X_train, y_train, epochs = self.epochs, batch_size = self.batchSize)
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
        mdl = nn.createModelStandard(X, Y, epochs = self.epochs, batch_size = self.batchSize)
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

        decisionWait = self.decisionWait
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

                decisionWait = decisionWait + 1
                if decisionWait >= self.decisionWait:
                    self.strategy.decide(lastKnownPrice, predict[-1], verbose=True)
                    decisionWait = 0

                retrainCount = retrainCount + 1
                if retrainCount >= self.retrainWait:
                    retrainCount = 0
                    data = self.stream.get()
                    cp = CandleProcessor(data, self.candleSize, self.LB)
                    mdl, scalerX, scalerY, lastKnown, X, Y = self.train(cp)
                    print "Train until candle: " + str(lastKnown)

            lastKnown = lastCandle
            time.sleep(10)
