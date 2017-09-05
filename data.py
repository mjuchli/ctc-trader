import math
import numpy
import pandas
from sklearn.preprocessing import MinMaxScaler

def financialDataset(column, path = 'data/price/bitstampUSD-30d-interval-1min.csv'):
        dataframe = pandas.read_csv(path, usecols=[column], engine='python', skipfooter=3)
        dataset = dataframe.values
        dataset = dataset.astype('float32')
        return dataset

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=10, labelled=True, label_ahead = 0):
        dataX, dataY = [], []
        # Note that if the look_back is larger than the dataset,
        # the ultimate dataset will be empty as no such look_back
        # vector can be built.
        assert len(dataset) >= look_back + label_ahead, "Dataset smaller than look_back + label_ahead"
        if labelled:
            r = range(len(dataset)-(look_back)-label_ahead)
        else:
            r = range(len(dataset)-(look_back-1))
        for i in r:
                a = dataset[i:(i+look_back), :]
                dataX.append(a)
                if labelled:
                    dataY.append(dataset[i + look_back + label_ahead-1, 0])
                else:
                    dataY.append(None)
        return numpy.array(dataX), numpy.array(dataY)

def createInputData(dataset, trainTestRatio = 0.67, look_back = 10, scaler = None):
        # normalize the dataset
        #### We should be aware that normalising over the whole range of data is not feasible in real life,
        #### since future data could fall outside the historical range
        #scaler = MinMaxScaler(feature_range=(0, 1))
        if scaler:
                dataset = scaler.fit_transform(dataset)

        # Ensures that the array is from Pandas regardless of Scaler
        dataset = numpy.array(dataset)

        ### We should think about the interplay between this look_back value and the LSTM units.
        ### Both form a way of incorporating historical data.
        X, Y = create_dataset(dataset, look_back)
        #X = numpy.reshape(X, (X.shape[0], X.shape[1], 1)) # [n x look_back]

        # split into train and test sets
        train_size = int(len(X) * trainTestRatio)
        test_size = len(X) - train_size

        trainX, testX = X[0:train_size,:], X[train_size:len(dataset),:]
        trainY, testY = Y[0:train_size], Y[train_size:len(dataset)]

        assert len(trainX) > 0, "Train Set empty"
        assert len(testX) > 0, "Test Set empty"
        #assert len(testX) >= 15, "Test set below 15 minute barrier"
        return (dataset, scaler, trainX, trainY, testX, testY)


def combineTrainTestFeatures(trainFeatures, testFeatures):
        trainX = numpy.dstack(trainFeatures)
        testX = numpy.dstack(testFeatures)
        print trainX.shape
        print testX.shape
        # Except of the number of elements,
        # training and test data has to be in the same format
        assert(trainX.shape[1] == testX.shape[1])
        #assert(trainX.shape[2] == testX.shape[2])
        return (trainX, testX)
