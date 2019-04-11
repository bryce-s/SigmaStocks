import sys
import os
import feedparser
import json
import csv
import re
from tickerHandler import Ticker

def check_type(*arg):
    """checks types of sucessive args"""
    assert len(arg) % 2 == 0
    for i in range(0, len(arg)-1):
        if i % 2 == 0:
           assert isinstance(arg[i], arg[i+1])

class TitleInfo:
    """stores an array of titles and any associated data we may want"""
    def __init__(self):
        self.titles = set()

    def push_title(self, title: frozenset):
        """pushes a title (represented inside a frozenset object)"""
        check_type(title, frozenset)
        self.titles.add(title)

    def get_titles(self):
        """returns all title dicts for a given ticker"""
        resDicts = list()
        for item in self.titles:
            resDicts.append(dict(item))
        return resDicts



class TickerToInfo:
    """cleanly maps ticker to ticker info, no dict abuse required"""
    def __init__(self):
        self.ticker_to_info = dict()

    def add_title(self, ticker: str, title: frozenset):
        check_type(title, frozenset, ticker, str)
        if ticker not in self.ticker_to_info:
            self.ticker_to_info[ticker] = TitleInfo()
            self.ticker_to_info[ticker].push_title(title)
        else:
            self.ticker_to_info[ticker].push_title(title)
        
    def get_titles_for_ticker(self, ticker: str):
        return self.ticker_to_info[ticker].get_titles()



class RssFetcher:
    """grabs rss things"""
    def __init__(self, input_company_list: str = "./target_news_sources.json"):
        assert isinstance(input_company_list, str)
        self.companies = str(input_company_list)

    def __process_tickers(self, ti: Ticker, all_tickers: dict, article_title: str, target: dict, ticker_info: TickerToInfo):
        for ticker in all_tickers:
            company_name = ti.get_company_name(ticker)
            # is company name in article_title? Is the fuxzy match score high
            article_title2 = re.sub(r'[^a-zA-Z0-9\s]+', '', article_title)
            company_name = re.sub(r'[^a-zA-Z0-9\s]+', '', company_name)
            company_name = company_name.lower()
            company_name = re.sub("(\scorp.)|(\scorp)|(\scorporation)|(\sinc.)|(\sthe)|(\scompany)|(\sinc)","",company_name)
            company_name = re.sub("[ \t]+$","", company_name) # remove trailing whitespace
            cname = ti.get_company_name(ticker)
            if " " + company_name in " " + article_title2.lower() or " " + ticker.lower() + " " in " " + article_title2.lower() + " ":
                print("match: " + cname)
                titleDict = dict()
                try:
                    titleDict['title'] = target['title']
                    titleDict['date'] = target['published']
                    titleDict['summary'] = target['summary']
                    titleDict['link'] = target['link']
                except KeyError as e:
                    continue
                fs = frozenset(titleDict.items())
                ticker_info.add_title(ticker.lower(), fs)






    def fetch_from_feed(self, ticker_info: TickerToInfo):
        check_type(ticker_info, TickerToInfo)
        json_object = open(self.companies, "r")
        rss_targets = json.load(json_object)
        target_count = 0
        for target in rss_targets.keys():
            # for each json object
            target_count += 1
            # for each news source and rss link combo
            news_source = rss_targets[target]['news_source']
            feed_link = rss_targets[target]['rss_link']
            feed = feedparser.parse(feed_link)
            feed_items = feed['items']
            for fi in feed_items:
                if 'published' in fi and 'title' in fi:
                    article_title = fi['title']
                    date = fi['published']
                    ti = Ticker()
                    all_tickers = ti.ticker_dict
                    # o(n^2) (more or less)
                    self.__process_tickers(ti, all_tickers, article_title, fi, ticker_info)
                  


def main():
    """we normally shouldn't have a main for this module.."""
    fetchbryce = RssFetcher() 
    info = TickerToInfo()
    fetchbryce.fetch_from_feed(info)

main()
