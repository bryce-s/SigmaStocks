import csv
import datetime
import linecache
import sys

from .analyzer import get_average_sentiment
from .prediction import predictData
from .stock import Stock_Obj

# Global variables to decide which stocks should be held if negative / track history for past day
prevDayStocks = []
holdStocks = []

numPositiveInvestment = 0
numNegativeInvestment = 0


# Exception printer
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


# Figuring out how much to invest given balance
def getNumInvest(balance):
    if balance < 5000:
        return 3
    if balance < 10000:
        return 4
    if balance < 20000:
        return 5
    return 6


# Figuring out how much to invest given balance and holding
def getNumInvestHolding(balance):
    holding = len(holdStocks)
    if balance < 5000:
        return 3 - holding
    if balance < 10000:
        return 4 - holding
    if balance < 20000:
        return 5 - holding
    return 6 - holding


# Figuring out how much to invest in each stock given balance
def getInvestmentAmount(balance):
    if balance < 5000:
        return 350
    if balance < 10000:
        return 1000
    if balance < 20000:
        return 2500
    return 3000


# Analyser for each day
def analyse(currentDayValues, currentDate, numInvest):
    global prevDayStocks, holdStocks, numCorrect, numWrong
    results = {}

    # Iterate through current day and average sentiment

    for stock in currentDayValues.keys():
        try:
            year = int(currentDate[0:4])
            month = int(currentDate[4:6])
            day = int(currentDate[6:8])
            date = datetime.datetime(year=year, month=month, day=day)
            pred = predictData(stock, 1, date)
            sentiment = get_average_sentiment(currentDayValues[stock])
            val = pred * sentiment
            if val > 0:
                if stock not in prevDayStocks:
                    results[stock] = val
        except:
            pass

    # Sort results to find top numInvest

    results_sorted = list(
        {k: v for k, v in sorted(results.items(), key=lambda x: x[1])})
    if numInvest > len(results_sorted):
        numInvest = len(results_sorted)
    topNumInvest = results_sorted[:numInvest]
    # topNumInvest = results_sorted[:numInvest] + holdStocks
    prevDayStocks = topNumInvest
    return topNumInvest


if __name__ == "__main__":
    numPositiveInvestment = 0
    numNegativeInvestment = 0
    numCorrect = 0
    numWrong = 0 
    balance = 1000

    history = open('../data/history.csv', 'w')
    reader = csv.DictReader(open('../data/sorted_news.csv'))
    next(reader)

    # Dictionary for current day values

    currentDayValues = dict()
    currentDate = None

    # Iterate through scraped news

    for row in reader:
        if balance > 0.01:

            # Capture news for date

            if currentDate == None:
                currentDate = row['date']
            if currentDate == row['date']:
                ticker = row['ticker']
                if ticker in currentDayValues.keys():
                    currentDayValues[ticker].append(row['headline'])
                else:
                    currentDayValues[ticker] = [row['headline']]
            else:
                try:
                    res = analyse(currentDayValues, currentDate,
                                  getNumInvest(balance))
                    dayIncome = 0
                    # holdStocks = []
                    # holdTemp = {}

                    # Code for calculating P/L for backtracer
                    for s in res:
                        obj = Stock_Obj(s)
                        historical = obj.getHistoricalPrice(currentDate)

                        # if historical:
                        #     diff = float(historical['close']) - float(historical['open'])
                        #         holdTemp[s] = diff
                        #     print(s, round(diff, 2), getInvestmentAmount(balance),
                        #           ((getInvestmentAmount(balance)) * diff), ' ')
                        #     dayIncome += ((getInvestmentAmount(balance)) * diff)

                        # Calculating diff

                        diff = float(historical['close']) - \
                               float(historical['open'])
                        if diff < 0:
                            numNegativeInvestment += 1
                        else:
                            numPositiveInvestment += 1
                        print(s, round(diff, 2), getInvestmentAmount(balance),
                              ((getInvestmentAmount(balance)) * diff), ' ')

                        # Add to day's income

                        dayIncome += ((getInvestmentAmount(balance)) * diff)

                    # Calculating growth and balance
                    growth = dayIncome / getInvestmentAmount(balance)
                    balance += dayIncome
                    out = currentDate + ', ' + \
                          str(res) + ', ' + str(balance) + \
                          ', ' + str(growth) + '\n'
                    history.write(out)
                    print(out)
                except:
                    PrintException()

                # Reset

                currentDate = row['date']
                currentDayValues = dict()
                currentDayValues[row['ticker']] = [row['headline']]
    print('Number Positive Investment: ', numPositiveInvestment)
    print('Number Negative Investment: ', numNegativeInvestment)
    print('Accuracy:', 100 * numPositiveInvestment / (numPositiveInvestment + numNegativeInvestment), '%', ' ')
    history.close()
