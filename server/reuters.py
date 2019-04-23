#!/usr/bin/env python3
"""
Crawl news headlines from Reuters and save as csv.
Input file: ./input/tickerList.csv
News append to: ./input/news_reuters.csv
"""
import datetime
import inspect
import os
import sys
import time
from urllib.request import urlopen

import numpy as np
from bs4 import BeautifulSoup

# credit: https://stackoverflow.com/a/11158224/4246348

currentDirectory = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.insert(0, parentDirectory)


class ReutersCrawler:

    def __init__(self):
        self.tickerFile = '../data/tickerList.csv'
        self.newsFile = '../data/news_reuters.csv'

    # Fetching news
    def fetchContent(self, task, date_range):
        ticker, name, exchange = task
        print("%s - %s - %s" % (ticker, name, exchange))

        suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
        url = "https://www.reuters.com/finance/stocks/company-news/" + \
              ticker + suffix[exchange]

        numNews = self.getNews(url)
        if numNews:
            retreievedNews, numNoNews = self.fetchWithinRange(
                numNews, url, date_range, task, ticker)
            if not retreievedNews:
                print('%s has no content within date range' % ticker)

    def scraper(self, url, verbose=True):
        for i in range(3):
            try:
                time.sleep(np.random.poisson(3))
                response = urlopen(url)
                data = response.read().decode('utf-8')
                return BeautifulSoup(data, "lxml")
            except Exception as e:
                print(e)

    def getNews(self, url):
        scraped = self.scraper(url)
        if scraped:
            return len(scraped.find_all("div", {'class': ['topStory', 'feature']}))
        return 0

    def fetchWithinRange(self, news_num, url, date_range, task, ticker):
        noNewsDays = 0
        newNews = False
        noNewNewsDay = []
        for timestamp in date_range:
            print('trying ' + timestamp, end='\r', flush=True)
            new_time = timestamp[4:] + timestamp[:4]
            soup = self.scraper(url + "?date=" + new_time)
            if soup and self.writeNews(
                    soup, task, ticker, timestamp):
                noNewsDays = 0
                newNews = True
            else:
                noNewsDays += 1

            if noNewsDays > news_num * 5 + 20:
                print("%s has no news for %d days, stop this candidate ..." %
                      (ticker, noNewsDays))
                break
            if noNewsDays > 0 and noNewsDays % 20 == 0:
                noNewNewsDay.append(timestamp)

        return newNews, noNewNewsDay

    def writeNews(self, soup, task, ticker, timestamp):
        content = soup.find_all("div", {'class': ['topStory', 'feature']})
        if not content:
            return False
        with open(self.newsFile, 'a+', newline='\n') as fout:
            for i in range(len(content)):
                title = content[i].h2.get_text().replace(",", " ").replace("\n", " ")
                body = content[i].p.get_text().replace(",", " ").replace("\n", " ")

                if i == 0 and soup.find_all("div", class_="topStory"):
                    news_type = 'topStory'
                else:
                    news_type = 'normal'

                print(ticker, timestamp, title, news_type)
                fout.write(','.join([ticker, task[1], timestamp, title, body, news_type]) + '\n')
        return True

    def generate_past_n_days(self, numdays):
        """Generate N days until now, e.g., [20151231, 20151230]."""
        base = datetime.datetime.today()
        date_range = [
            base - datetime.timedelta(days=x) for x in range(0, numdays)]

        return [x.strftime("%Y%m%d") for x in date_range]

    def run(self, numdays=60):
        """Start crawler back to numdays"""
        date_range = self.generate_past_n_days(60)

        with open(self.tickerFile) as ticker_list:
            for line in ticker_list:
                task = tuple(line.strip().split(','))
                ticker, name, exchange = task
                self.fetchContent(task, date_range)


def main():
    reuter_crawler = ReutersCrawler()
    reuter_crawler.run(60)


if __name__ == "__main__":
    main()
