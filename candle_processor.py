import numpy as np
from sklearn.preprocessing import MinMaxScaler
from enum import Enum

class LabelType(Enum):
    NoLabel = 'No label'
    ClosingPrice = 'Closing Price'
    Direction = 'Direction change'
    Direction1Pc = 'Direction 1%'

class CandleProcessor:
    def __init__(self, candles, candle_size, look_back):
        self.candles = candles
        self.candle_size = candle_size
        self.look_back = look_back
        self.scalerX = None
        self.scalerY = None

    @staticmethod
    def non_shuffling_train_test_split(X, y, test_size=0.1):
        i = int((1 - test_size) * X.shape[0]) + 1
        X_train, X_test = np.split(X, [i])
        y_train, y_test = np.split(y, [i])
        return X_train, X_test, y_train, y_test

    # convert an array of values into a dataset matrix
    def features_to_data_set(self, features, labels=[]):
        dataX, dataY = [], []
        if labels:
            assert len(features) >= self.look_back + self.candle_size, "Dataset smaller than look_back + candle_size"
            r = range(len(features)-(self.look_back)-self.candle_size)
        else:
            assert len(features) >= self.look_back, "Dataset smaller than look_back"
            r = range(len(features)-(self.look_back-1))
        for i in r:
            a = features[i:(i+self.look_back), :]
            dataX.append(a)
            if labels:
                dataY.append(labels[i + self.look_back + self.candle_size-1])
            else:
                dataY.append(None)
        return np.array(dataX), np.array(dataY)

    def get_feature_set(self):
        dataArray = [[float(x.close), # first element serves as Y
                      float(x.open),
                      float(x.high),
                      float(x.low),
                      float(x.trades),
                      float(x.volume)
                      # mean price
                      # last 15m, 30, 45, 1h, 3h, 6h, 1w... price change
                      # time of the day (normalized time of the day)
                      # days (binary)
                      # bid / ask volume
                      # bid / ask volume since Xmin
                      ] for x in self.candles]
        return np.array(dataArray)

    def get_data_set(self, scaled = False, labelType = LabelType.ClosingPrice):
        features = self.get_feature_set()
        labels = self.get_y(labelType)

        if scaled:
            features, scalerX = self.scale_x(features)
            if labelType == LabelType.ClosingPrice:
                labels, scalerY = self.scale_y(labels)
                labels = labels.tolist()
            else:
                scalerY = None
        else:
            scalerX = None
            scalerY = None

        X, Y = self.features_to_data_set(features, labels)
        return (X, Y, scalerX, scalerY)

    def get_data_set_unlablled(self, scaled = False):
        """ Reduced data set which contains only samples for which no labels exist yet. """
        X_labelled, _, _, _ = self.get_data_set(scaled, LabelType.ClosingPrice)
        idx = len(X_labelled)
        (X, Y, scalerX, scalerY) = self.get_data_set(scaled, LabelType.NoLabel)
        return (X[idx:], Y[idx:], scalerX, scalerY)

    def get_y(self, labelType):
        if labelType == LabelType.NoLabel:
            labels = []
        elif labelType == LabelType.ClosingPrice:
            labels = self.get_y_closing()
        elif labelType == LabelType.Direction:
            labels = self.get_y_direction()
        elif labelType == LabelType.Direction1Pc:
            labels = self.get_y_direction_1pc()
        return labels

    def get_y_closing(self):
        """ Closing Price as label """
        ys = [x[0] for x in self.get_feature_set()]
        return ys

    def get_y_direction(self):
        """label according to direction change
        0:  same price as last candle
        1:  price greater than last candle closing price
        -1: price smaller than last candle closing price
        """
        ys = self.get_y_closing()
        ysd = [0]
        for i in range(0, len(ys)-1):
            if ys[i+1] > ys[i]:
                ysd.append(1)
            # elif ys[i+1] == ys[i]:
            #     ysd.append(0)
            else:
                ysd.append(0)
        return ysd

    def get_y_direction_1pc(self):
        """more than 1 percent direction change, see get_y_direction for return"""
        ys = self.get_y_closing()
        ysd = [0]
        for i in range(0, len(ys)-1):
            pc = float(ys[i+1]) / float(ys[i])
            if pc >= 1.01:
                ysd.append(1)
            elif pc <= 0.99:
                ysd.append(-1)
            else:
                ysd.append(0)
        return ysd

    def scale_x(self, xs):
        if self.scalerX:
            data = self.scalerX.fit_transform(xs)
        else:
            scaler = MinMaxScaler(feature_range=(0, 1))
            data = scaler.fit_transform(xs)
            self.scalerX = scaler
        return (data, self.scalerX)

    def scale_y(self, xs):
        if self.scalerY:
            data = self.scalerY.fit_transform(xs)
        else:
            scaler = MinMaxScaler(feature_range=(0, 1))
            data = scaler.fit_transform(xs)
            self.scalerY = scaler
        return (data, self.scalerY)
