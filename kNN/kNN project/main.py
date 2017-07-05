import csv
import math
import operator
import time

import plotly.plotly as py
from plotly.graph_objs import *
from sympy.printing.tests.test_numpy import np


def loadData(trainingDataSource, testDataSource, trainingSet, testSet):
    # Load training data
    with open(trainingDataSource, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataSet = list(lines)
        for x in range(len(dataSet) - 1):
            for y in range(4):
                dataSet[x][y] = float(dataSet[x][y])
            trainingSet.append(dataSet[x])
    # Load values that need to be tested
    with open(testDataSource, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataSet = list(lines)
        for x in range(len(dataSet) - 1):
            for y in range(4):
                dataSet[x][y] = float(dataSet[x][y])
            testSet.append(dataSet[x])


def distanceEuclid(object1, object2, numOfAttrib):
    distance = 0
    for x in range(numOfAttrib):
        distance += pow((object1[x] - object2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = distanceEuclid(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getRepeatedCount(neighbors, showOccurances=True):
    # dictionary with occurrences
    classOccurrences = {}
    for x in range(len(neighbors)):
        className = neighbors[x][-1]
        if className in classOccurrences:
            # iterate existing class
            classOccurrences[className] += 1
        else:
            # add new if doesnt exist
            classOccurrences[className] = 1
    classOccurrencesSorted = sorted(classOccurrences.items(), key=operator.itemgetter(1), reverse=True)
    if showOccurances:
        print('Classes in neighbourhood: ')
        print(classOccurrencesSorted)

    # In case two results having same number of occurances we pick the one that has lower distance
    if len(classOccurrencesSorted) > 1 and classOccurrencesSorted[0][1] == classOccurrencesSorted[1][1]:
        for x in range(len(neighbors)):
            if neighbors[x][-1] == classOccurrencesSorted[0][0]:
                return neighbors[x][-1]
            elif neighbors[x][-1] == classOccurrencesSorted[1][0]:
                return neighbors[x][-1]

    else:
        return classOccurrencesSorted[0][0]


def getAccuracy(testSet, predictedValues):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictedValues[x]:
            correct += 1
    return (correct / len(testSet)) * 100.0


def getAccuracyForK(testSet, trainingSet, k):
    predictedValues = []
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getRepeatedCount(neighbors, False)
        predictedValues.append(result)
    accuracy = getAccuracy(testSet, predictedValues)
    return accuracy


def createGraph(testSet, trainingSet):
    dataX = []
    dataY = []
    for x in range(1, len(trainingSet)):
        dataX.append(x)
        dataY.append(getAccuracyForK(testSet, trainingSet, x))

    trace1 = Scatter(
        x=dataX,
        y=dataY,
        mode='markers',
        name="Actual Value"
    )

    z = np.polyfit(dataX, dataY, 3)
    f = np.poly1d(z)

    x_new = np.linspace(dataX[0], dataX[-1], 50)
    y_new = f(x_new)

    trace2 = Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        marker=Marker(color='rgb(0, 204, 0)'),
        name='Fit'
    )

    data = [trace1, trace2]
    layout = dict(title='Percentage of correctly classified test examples versus K',
                  xaxis=dict(title='K value [1]'),
                  yaxis=dict(title='Accuracy of kNN [%]'),
                  )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='kNN correct precentage versus K')


def estimateAndCompareActual(testSet, trainingSet):
    predictedValues = []
    try:
        k = int(input('Please enter number of neighbours to be checked (k value, needs to be lower than ' + repr(
            len(trainingSet)) + '):\n'))
        if k > len(trainingSet):
            print('K cannot be bigger than the current training set!')
            return
    except ValueError:
        print('K needs to be integer!')
        return

    startTime = time.time()
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getRepeatedCount(neighbors)
        predictedValues.append(result)
        print('test data set value  = ' + repr(testSet[x][-1]))
        print('kNN predicted value = ' + repr(result), end='')
        if result == testSet[x][-1]:
            print(' - correct!\n')
        else:
            print(' - incorrect!\n')
    accuracy = getAccuracy(testSet, predictedValues)
    print('Accuracy: ' + str(accuracy) + '%')
    endTime = time.time()
    print('Time to calculate: ' + repr(endTime - startTime) + ' s\n\n')


def testInputByUser(trainingSet):

    numberOfItems = int(input('Please enter number of items you are going to enter.\n'))
    testSet = []
    print('Enter values - Sepal.Length, Sepal.Width, Petal.Length, Petal.Width '
          'and test class (with single spaces in between)\n ')
    for x in range(numberOfItems):
        var1, var2, var3, var4, varClass = input().split()
        testSet.append([float(var1), float(var2), float(var3), float(var4), varClass])
    estimateAndCompareActual(testSet,trainingSet)


def main():
    # Load data
    trainingSet = []
    testSet = []
    loadData('train.txt', 'test.txt', trainingSet, testSet)
    print('Items in training set: ' + repr(len(trainingSet)))
    print('Items in test set: ' + repr(len(testSet)))

    while True:

        option = input(
            'Please choose mode: \n'
            'T - Run the tests for a given K\n'
            'D - Input data to get estimated class of the object,\n'
            'G - Plot percentage of correctly classified test examples versus K\nQ - Exit\n')
        option = option.upper()

        if option == 'Q':
            return
        elif option == 'T':
            estimateAndCompareActual(testSet, trainingSet)
        elif option == 'D':
            testInputByUser(trainingSet)
        elif option == 'G':
            createGraph(testSet, trainingSet)
            # https://plot.ly/~ThatGaskin/5/percentage-of-correctly-classified-test-examples-versus-k/

main()
