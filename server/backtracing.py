from analyzer import get_average_sentiment
from prediction import predictData
import csv
import datetime
from stock import Stock_Obj


prevDayStocks = []


def getNumInvest(balance):
    if balance < 5000:
        return 3
    if balance < 10000:
        return 4
    if balance < 20000:
        return 5
    return 6


def getInvestmentAmount(balance):
    if balance < 5000:
        return 350
    if balance < 10000:
        return 1000
    if balance < 20000:
        return 2500
    return 3000


def analyse(currentDayValues, currentDate, numInvest):
    global prevDayStocks
    results = {}
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
    results_sorted = list(
        {k: v for k, v in sorted(results.items(), key=lambda x: x[1])})
    if numInvest > len(results_sorted):
        numInvest = len(results_sorted)
    topNumInvest = results_sorted[:numInvest]
    prevDayStocks = topNumInvest
    return topNumInvest


if __name__ == "__main__":

    balance = 1000

    history = open('../data/history.csv', 'w')
    reader = csv.DictReader(open('../data/sorted_news.csv'))
    next(reader)
    currentDayValues = {}
    currentDate = None
    currentTicker = None
    for row in reader:
        if balance > 0.01:
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
                    for s in res:
                        obj = Stock_Obj(s)
                        historical = obj.getHistoricalPrice(currentDate)
                        diff = float(historical['close']) - \
                            float(historical['open'])
                        print(s, round(diff, 2), getInvestmentAmount(balance),
                              ((getInvestmentAmount(balance))*diff),  ' ')
                        dayIncome += ((getInvestmentAmount(balance))*diff)
                    growth = dayIncome / getInvestmentAmount(balance)
                    balance += dayIncome
                    out = currentDate + ', ' + \
                        str(res) + ', ' + str(balance) + \
                        ', ' + str(growth) + '\n'
                    history.write(out)
                    print(out)
                except:
                    pass
                currentDate = row['date']
                currentDayValues = {}
                currentDayValues[row['ticker']] = [row['headline']]
    history.close()
