#!/usr/bin/python
import sys
import os
import feedparser



def main():
    wsj_market_news_rrs = 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'
    feed = feedparser.parse(wsj_market_news_rrs)
    feed_items = feed['items']
    pass
    

main()


