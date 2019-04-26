import os
from datetime import datetime, timedelta

import numpy as np
from iexfinance.stocks import get_historical_data
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


# Linear regression for stocks

# Main driver for predictData, can take in a list etc
def getStocks(stockList, date=datetime.now()):
    for stock in stockList:
        predictData(stock, 5, date)


# Forecasts 5 days using 16 weeks as training to predict 5 days
def predictData(stock, numForecast=5, date=datetime.now()):
    start = date - timedelta(weeks=16)
    end = date

    # Get dataframe from IEX API

    df = get_historical_data(
        stock, start=start, end=end, output_format='pandas')

    # Generating static data file for stock

    if os.path.exists('../Data/StockData'):
        csv_name = ('../Data/StockData/' + stock + '_Prices.csv')
    else:
        if not os.path.exists("../Data/"):
            os.mkdir("../Data/")
        os.mkdir("../Data/StockData")
        csv_name = ('../Data/StockData/' + stock + '_Prices.csv')

    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    # Preparing features for linear regression

    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-numForecast:]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.5)

    # Generate linear regression

    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    # Returns normalised prediction to the stock's price (aka movement)

    return (prediction[0] - df['close'][1]) / df['close'][1]

def predict_pair(stock, numForecast=5, date=datetime.now()):
    start = date - timedelta(weeks=16)
    end = date

    # Get dataframe from IEX API

    df = get_historical_data(
        stock, start=start, end=end, output_format='pandas')

    # Generating static data file for stock

    if os.path.exists('../Data/StockData'):
        csv_name = ('../Data/StockData/' + stock + '_Prices.csv')
    else:
        if not os.path.exists("../Data/"):
            os.mkdir("../Data/")
        os.mkdir("../Data/StockData")
        csv_name = ('../Data/StockData/' + stock + '_Prices.csv')

    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    # Preparing features for linear regression

    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-numForecast:]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.5)

    # Generate linear regression

    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    # Returns normalised prediction to the stock's price (aka movement)

    return ((prediction[0] - df['close'][1]) / df['close'][1], prediction)


if __name__ == '__main__':
    getStocks(['GOOG'])
