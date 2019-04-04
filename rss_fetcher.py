import sys
import os
import feedparser
import json
import csv
from tickerHandler import Ticker


def add_json_dipyct(json_files_dict: dict, ticker: str, title: str, date: str):
    print(ticker)

def fetch_rss(filename: str):
    """return our JSON list, yes?"""
    json_object = open("./target_news_sources.json", "r")
    rss_targets = json.load(json_object)
    result_dict = dict()
    for target in rss_targets.keys():
        # for each news source and rss link combo
        news_source = rss_targets[target]['news_source']
        feed_link = rss_targets[target]['rss_link']
        feed = feedparser.parse(feed_link)
        feed_items = feed['items']
        date = None
        for fi in feed_items:
            if 'published' not in fi or 'title' not in fi:
                pass # do nothing :)
            else:
                t = Ticker()
                article_title = fi['title']
                for word in article_title.split():
                    if word in t.ticker_dict:
                        add_json_dict(result_dict, word, article_title, date)
                    else:
                     for company_name in t.ticker_dict.values():
                         if company_name in article_title:
                             add_json_dict(result_dict, company_name, article_title, date)
                # date = fi['published']
                # print('title: ' + article_title + ' published: ' + date)
        pass
    

fetch_rss("w")

