import sys
import re

res = re.findall(r'>\w+<', open("./result_tickers.txt").read())
for result in res:
    ticker_str = result[1:len(result)-1]
    print(ticker_str)
