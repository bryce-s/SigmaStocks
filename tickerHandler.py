import csv
import sys
from urllib.request import urlopen


def get_tickers(exchangeList=["NASDAQ", "NYSE", "AMEX"], debug=False):
    assert isinstance(exchangeList, list)
    assert isinstance(debug, bool)
    ticker_list = open('tickerList.csv', 'w')
    writer = csv.writer(ticker_list, delimiter=',')
    output = []
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        try:
            if debug:
                print("Downloading tickers from {}...".format(exchange))
            response = urlopen(url + exchange + '&render=download')
            content = response.read().decode('utf-8').split('\n')
            for num, line in enumerate(content):
                line = line.strip().strip('"').split('","')
                if num == 0 or len(line) != 9:
                    continue
                output.append([line[0], line[1]])
            break
        except:
            continue
    for data in output:
        writer.writerow(data)
