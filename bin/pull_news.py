import sys
import os
import re
from sty import fg
import requests
import json


def typecheck(obj, t):
    assert isinstance(obj, t)


class StockNewsPuller:
    """pulls articles from stocknewsapi and packages them into json"""

    def __init__(self):
        self.api_key = open("./stocknews_key.txt", "r").read()
        self.all_ticker_targets = open("./tickers.txt", "r").read()
        self.api_string = "https://stocknewsapi.com/api/v1?tickers={}&items={}&token={}"

    def pull_articles(self, tickers: str):
        """pulls articles from the API and returns filename to resulting JSON
        Should be formatted in CSV, e.g. TSLA,AMZN,FB"""
        # print(fg.red + "we are using an api call!" + fg.rs)
        typecheck(tickers, str)
        target_str = self.api_string.format(tickers, 50, self.api_key)
        data_json = requests.get(target_str).json()
        json_str = json.dumps(data_json, sort_keys=True, indent=4)
        with open("./pull_news_out.json", "w+") as outFile:
            outFile.write(json_str)


stp = StockNewsPuller()
stp.pull_articles("TSLA")
