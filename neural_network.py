from keras.models import Sequential
from keras.models import Model
from sklearn.linear_model import SGDRegressor
from keras.layers import Dense, Dropout, LSTM, SimpleRNN, Embedding, Input, TimeDistributed

# create and fit the LSTM network
# we can build some sort of an interface to try out multiple variants
def createModelStandard(trainX, trainY, epochs = 10, batch_size = 1000):
    model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
    model.add(LSTM(int(trainX.shape[1])*int(trainX.shape[2]), input_shape=(trainX.shape[1], trainX.shape[2]), activation='tanh', recurrent_activation='tanh'))
    model.add(Dense(int(trainX.shape[1])*int(trainX.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
    return model

def createModelBinary(trainX, trainY, epochs = 10, batch_size = 1000):
    print trainX.shape
    print trainX
    model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
    model.add(LSTM(int(trainX.shape[1])*int(trainX.shape[2]), input_shape=(trainX.shape[1], 1), return_sequences=True))
    #model.add(Dense(int(trainX.shape[1])*int(trainX.shape[2])))
    model.add(TimeDistributed(Dense(1, activation='sigmoid')))
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
    return model

def createSimpleRNN(trainX, trainY, epochs = 10, batch_size=1000):
        model = Sequential()
        model.add(SimpleRNN(int(trainX.shape[1]) * int(trainX.shape[2]), input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(int(trainX.shape[1]) * int(trainX.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createTwoLayerHidden(trainX, trainY, epochs = 10, batch_size=1000):
        model = Sequential()
        model.add(SimpleRNN(int(trainX.shape[1]) * int(trainX.shape[2]), input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(int(trainX.shape[1]) * int(trainX.shape[2])))
        #Add another layer with half the neurons
        model.add(Dense(int(trainX.shape[1]) * int(trainX.shape[2])) * 0.5)
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM10(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(10, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM100(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM50(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(50, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM10DENSE10(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(10, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(10))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM100DENSE100(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(100))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM50DENSE50(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(50, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM10DENSE10DENSE5(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(10, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(10))
        model.add(Dense(5))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM100DENSE100DENSE5(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(100))
        model.add(Dense(5))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM50DENSE50DENSE5(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(50, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(50))
        model.add(Dense(5))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM500DENSE500(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(500, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(500))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM500DENSE500DENSE50(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(500, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(500))
        model.add(Dense(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM1000DENSE1000(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(1000, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(1000))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def createLSTM1000DENSE1000DENSE50(trainX, trainY, epochs = 20, batch_size = 1000):
        model = Sequential()
    # shape[1] is equivalent to nr. of features
    # shape[2] is equivalent to look_back
        model.add(LSTM(1000, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dense(1000))
        model.add(Dense(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=2)
        return model

def getModels(trainX, trainY):
        batchSize = 100
        epochs = 25
        return [
                ("1-Layer LSTM", createModelStandard(trainX, trainY, epochs, batchSize)),
                # ("LSTM10", createLSTM10(trainX, trainY, epochs, batchSize)),
        # ("LSTM50", createLSTM50(trainX, trainY, epochs, batchSize)),
                # ("LSTM100", createLSTM100(trainX, trainY, epochs, batchSize)),
                # ("LSTM10DENSE10", createLSTM10DENSE10(trainX, trainY, epochs, batchSize)),
                # ("LSTM50DENSE50", createLSTM50DENSE50(trainX, trainY, epochs, batchSize)),
        # ("LSTM500DENSE500", createLSTM500DENSE500(trainX, trainY, epochs, batchSize)),
        # ("LSTM500DENSE500D/ENSE50", createLSTM500DENSE500DENSE50(trainX, trainY, epochs, batchSize)),
        # ("LSTM1000DENSE1000", createLSTM1000DENSE1000(trainX, trainY, epochs, batchSize)),
        # ("LSTM1000DENSE1000DENSE50", createLSTM1000DENSE1000DENSE50(trainX, trainY, epochs, batchSize)),
        # ("LSTM100DENSE100", createLSTM100DENSE100(trainX, trainY, epochs, batchSize)),
                # ("LSTM10DENSE10DENSE5", createLSTM10DENSE10DENSE5(trainX, trainY, epochs, batchSize)),
                # ("LSTM100DENSE100DENSE5", createLSTM100DENSE100DENSE5(trainX, trainY, epochs, batchSize)),
                # ("LSTM50DENSE50DENSE5", createLSTM50DENSE50DENSE5(trainX, trainY, epochs, batchSize))
        ]
