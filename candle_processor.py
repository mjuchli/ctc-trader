import numpy as np
from sklearn.preprocessing import MinMaxScaler

class CandleProcessor:
    def __init__(self, candles, candle_size, look_back):
        self.candles = candles
        self.candle_size = candle_size
        self.look_back = look_back
        self.scaler = None

    @staticmethod
    def non_shuffling_train_test_split(X, y, test_size=0.1):
        i = int((1 - test_size) * X.shape[0]) + 1
        X_train, X_test = np.split(X, [i])
        y_train, y_test = np.split(y, [i])
        return X_train, X_test, y_train, y_test

    # convert an array of values into a dataset matrix
    def features_to_data_set(self, features, labelled=True):
        dataX, dataY = [], []
        if labelled:
            assert len(features) >= self.look_back + self.candle_size, "Dataset smaller than look_back + candle_size"
            r = range(len(features)-(self.look_back)-self.candle_size)
        else:
            assert len(features) >= self.look_back, "Dataset smaller than look_back"
            r = range(len(features)-(self.look_back-1))
        for i in r:
            a = features[i:(i+self.look_back), :]
            dataX.append(a)
            if labelled:
                dataY.append(features[i + self.look_back + self.candle_size-1, 0])
            else:
                dataY.append(None)
        return np.array(dataX), np.array(dataY)

    def get_feature_set(self):
        dataArray = [[float(x.close), # first element serves as Y
                      float(x.open),
                      float(x.high),
                      float(x.low),
                      float(x.trades),
                      float(x.volume)] for x in self.candles]
        return np.array(dataArray)

    def get_data_set(self, scaled = False, labelled = True):
        if scaled:
            features, scalerX = self.scale(self.get_feature_set())
            X, Y = self.features_to_data_set(features, labelled)
            _, scalerY = self.get_y(True)
        else:
            scalerX = None
            scalerY = None
            X, Y = self.features_to_data_set(self.get_feature_set(), labelled)
        return (X, Y, scalerX, scalerY)

    def get_data_set_unlablled(self, scaled = False):
        X_labelled, _, _, _ = self.get_data_set(scaled, labelled = True)
        idx = len(X_labelled)
        (X, Y, scalerX, scalerY) = self.get_data_set(scaled, labelled = False)
        return (X[idx:], Y[idx:], scalerX, scalerY)

    def get_y(self, scaled = False):
        ys = [x[0] for x in self.get_feature_set()]
        if scaled:
            return self.scale(ys)
        return ys

    def get_y_direction(self, shift = 1):
        """label according to direction change
        0:  same price as last candle
        1:  price greater than last candle closing price
        -1: price smaller than last candle closing price
        """
        ys = [x[0] for x in self.get_feature_set()]
        ysd = [0]
        for i in range(0, len(ys)-shift):
            if ys[i+shift] > ys[i]:
                ysd.append(1)
            elif ys[i+shift] == ys[i]:
                ysd.append(0)
            else:
                ysd.append(-1)
        return ysd

    def get_y_direction_1pc(self, shift = 0):
        """more than 1 percent direction change, see get_y_direction for return"""
        ys = [x[0] for x in self.get_feature_set()]
        ysd = [0]
        for i in range(0, len(ys)-1-shift):
            pc = float(ys[i+shift]) / float(ys[i])
            if pc >= 1.01:
                ysd.append(1)
            elif pc <= 0.99:
                ysd.append(-1)
            else:
                ysd.append(0)
        return ysd

    def scale(self, xs):
        if self.scaler:
            data = self.scaler.fit_transform(xs)
        else:
            scaler = MinMaxScaler(feature_range=(0, 1))
            data = scaler.fit_transform(xs)
            self.scaler = scaler
        return (data, self.scaler)
