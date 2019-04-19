import numpy as np
from datetime import datetime, timedelta
import os
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from iexfinance.stocks import get_historical_data

def getStocks(stockList, date=datetime.now()):
    for stock in stockList:
        predictData(stock, 5, date)

def predictData(stock, numForecast=5, date=datetime.now()):
    start = date - timedelta(weeks=8)
    end = date
    df = get_historical_data(stock, start=start, end=end, output_format='pandas')
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

    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-numForecast:]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.5)
        
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    return (prediction[0] - df['close'][1]) / df['close'][1]

    # print(stock)
    # print(prediction)
    # print(getMovement(prediction, df.tail(1)['close']))

    # print('-----------------------------------------------------------------------')

if __name__ == '__main__':
    getStocks(['GOOG'])