import numpy
import math
import matplotlib.pyplot as plt
import pandas
from sklearn.metrics import mean_squared_error

def getRMSE(Y, predict):
    return math.sqrt(mean_squared_error(Y, predict))

def printRMSE(Y, predict):
    print('Test Score: %.2f RMSE' % (getRMSE(Y, predict)))

# Returns ratio of how often the model predicted the correct "direction" (up/down)
def directionRatio(prices, predict, timeSteps = 0):
    #assert(len(predict) == len(prices))
    correct = 0
    # Set default to entire range
    if timeSteps == 0:
        timeSteps = len(prices)
    for i in range(0,timeSteps-1):
        if (predict[i] > prices[i] and prices[i+1] > prices[i]) or (predict[i] < prices[i] and prices[i+1] < prices[i]) or (predict[i] == prices[i] and prices[i+1] == prices[i]):
            correct += 1
    return float(correct)/float(timeSteps)

def printDirectionRatio(prices, predict, timeSteps = 0):
    print('Direction (UP/DOWN) ratio: %.2f' % (directionRatio(prices, predict, timeSteps)))

def getDirectionRatioChange(prices, predict, timeSteps = 0):
	assert (len(predict) == len(prices))
	correct = 0
	if timeSteps == 0:
		timeSteps = len(prices)
	for i in range(0, timeSteps - 1):
		if (predict[i] > 0 and prices[i+1] > 0) or (
				predict[i] < 0 and prices[i + 1] < 0 or
				predict[i] == 0 and prices[i + 1] == 0) :
			correct += 1
	return float(correct) / float(len(predict))

def printDirectionRatioChange(prices, predict, timeSteps = 0):
    print('Direction (Positive / Negative) ratio: %.2f' % (getDirectionRatioChange(prices, predict, timeSteps)))

# Make a plot of the models prediction given testX and trainX
# and compare it to datasets acutal Y's.
def getModelPlot(dataX, dataY, trainPredict, testPredict):
    plt.close('all')
    # shift train predictions for plotting
    trainPredictPlot = numpy.empty((dataX.shape[0], 1))
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[0:len(trainPredict), :] = trainPredict[:, None]
    # shift test predictions for plotting
    testPredictPlot = numpy.empty((dataX.shape[0], 1))
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(trainPredict) - 1:len(dataY) - 1, :] = testPredict[:, None]
    # plot baseline and predictions
    plt.plot(dataY)
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    return plt

def topNModels(filenames, metrics, topN = 5):
	# Dict with metric_name: bool
    lowerBetter = dict((x,metrics[x][1]) for x in metrics.keys())
    # Dict with metric_name: col in tsv
    metricsCols = dict((x,metrics[x][0]) for x in metrics.keys())
    modelNames = []
    # Get model names e.g. 1-Layer LSTM 10 0.9975
    df = pandas.read_csv(filenames[0], sep='\t', header=None).iloc[:,0:4]; df
    modelNames = [df.iloc[x,0][7:]+' '+df.iloc[x,1][4:]+' '+df.iloc[x,2][9:]+' '+df.iloc[x,3][11:] for x in df.index];
    results = dict((x,[0]*len(modelNames)) for x in metrics.keys())

    for (i, filename) in enumerate(filenames):
        df = pandas.read_csv(filename, sep='\t', header=None)
        # For each model
        for m in range(len(df)):
        	# Add performance of a model in each metric to performances over previous datasets
            performance = df.iloc[m,[x for x in metricsCols.values()]]
            for x in metrics.keys():
                results[x][m] += performance[metricsCols[x]]

    bestModels = dict((x,y) for (x,y) in zip(metrics.keys(),[['']*topN]*3))

    # For each evaluation metric find the best performers
    for k in results.keys():
        results[k] = numpy.divide(results[k], len(filenames))
        # If minimising metric, then print first N
        if lowerBetter[k]:
            bestModels[k] = [modelNames[x] + ' - mean: ' + str(results[k][x]) for x in numpy.argsort(results[k])[:topN]]
        # If maximising metric, print last N best to worst
        else:
            bestModels[k] = [modelNames[x] + ' - ' + "mean: " + str(results[k][x]) for x in numpy.flip(numpy.argsort(results[k])[-topN:],0)]
    for k in metrics.keys():
        print "The best %d performers for " % topN + k
        for x in bestModels[k]:
            print x
        print '---'

def evaluateSelectedModels():
	import os
	metrics = {'rmse':(6, True), 'uds':(7,False), 'uds15':(8, False), 'profit':(9, False)}
	files = [("evaluation/Parameters/" + x) for x in os.listdir('evaluation/Parameters/') if x.startswith('backtest-new') and x.endswith('.tsv')]
	topNModels(files, metrics)
