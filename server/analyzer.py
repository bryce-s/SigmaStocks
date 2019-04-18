import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import decimal
import requests
import json
import sqlite3
from iexfinance.stocks import Stock
import datavide
from datetime import datetime
from rss_fetcher import RssFetcher, TickerToInfo
from prediction import predictData

# starting values and global portfolio values
starting_wealth = 1000000000

# function handles taking headline and returning sentiment score
def get_average_sentiment(input_list):
    sia = SentimentIntensityAnalyzer()
    total = 0.0
    size = len(input_list)

    for headline in input_list:
        intensity = sia.polarity_scores(headline)
        score = intensity["compound"]
        total += score

    if size != 0:
        average = round(total / size, 8)
        return(average)
    else:
        return(0)

# function handles updating the portfolio by retrieving new articles, recalculating sentiment, and changing position
def update_portfolio():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    # initialization of the RSS fetcher instance
    fetchbryce = RssFetcher()
    info = TickerToInfo()
    fetchbryce.fetch_from_feed(info, max_to_fetch=500)
    
    total_value = 0
    total_sentiment = 0
    num_invested = 0

    # get the opening value of the portfolio
    close_query = "select close from history order by day desc"
    last_value = c.execute(close_query).fetchone()
    last_value = last_value[0]
    
    # get the opening sentiment of the portfolio
    sent_query = "select close_sentiment from history order by day desc"
    last_sent = c.execute(sent_query).fetchone()
    last_sent = last_sent[0]
    
    # go through each ticker in the s&p 500
    # ticker, sentiment, price, shares
    #print(len(c.execute("select * from assets")))
    for row in c.execute("select * from assets").fetchall():
        # old portfolio information
        ticker = str(row[0])
        old_sentiment = row[1]
        old_price = row[2]
        old_shares = row[3]

        # get new information
        # get current stock price
        try:
            ticker_price = Stock(ticker).get_price()
        except:
            continue

        # datavide headlines
        headlines = datavide.datavide_headlines(ticker)
            
        # RSS article headlines
        try:
            rss_headlines = info.get_titles_for_ticker(ticker)
            print(type(rss_headlines))
            for ticker_obj in rss_headlines:
                headlines.append(ticker_obj['title'])
            # exit(1)
        except:
            pass

        # calculate average sentiment score for the article headlines of the given ticker
        new_sentiment = 0
        new_sentiment = get_average_sentiment(headlines)
        print(ticker + " " + str(new_sentiment))

        # set number of shares
        new_shares = 0

        # capitalization
        ticker_cap = 0
    
        prediction_difference = predictData(ticker, 5)
        # if ticker sentiment goes up by more than 0.05, buy more stock
        if new_sentiment - old_sentiment > 0.05 and prediction_difference > 0:
            # set number of shares
            new_shares = old_shares
            new_shares += 5
            print("good news")
            # capitalization
            ticker_cap = new_shares * ticker_price
            total_value += ticker_cap
            total_sentiment += new_sentiment
            num_invested += 1
        
        # else if ticker sentiment falls by more than 0.05, sell
        elif new_sentiment - old_sentiment < -0.05:
            # sell current chares
            num_shares = 0
            print("bad news")

        # sentiment didn't change, keep position the same
        else:
            if old_shares > 0:
                # capitalization
                print("no news")
                new_shares = old_shares
                ticker_cap = new_shares * ticker_price
                total_value += ticker_cap
                total_sentiment += new_sentiment
                num_invested += 1                

        # insert into the database, we will still put assets into the database we do not have positions in
        query_string = "update assets set sentiment={}, price={}, shares={} where ticker='{}'".format(new_sentiment, ticker_price, new_shares, ticker)
        c.execute(query_string)
        conn.commit()

    # update our overview table
    current_time = str(datetime.today())
    current_value = total_value
    current_sentiment = total_sentiment / num_invested
    open_value = current_value
    open_sentiment = current_sentiment
    value_change = ticker_price - old_price
    sentiment_change = new_sentiment - old_sentiment
    history_query = "insert into history values('{}', {}, {}, {}, {}, {}, {}, {})".format(current_time, last_value, current_value, last_sent, current_sentiment, value_change, sentiment_change, num_invested)
    c.execute(history_query)
    conn.commit()

    print(total_value)
    conn.close()

# function handles the initialization of the portfolio
def initialize_portfolio():
    
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    global starting_wealth
    total_value = 0
    total_sentiment = 0
    num_invested = 0

    # initialization of the RSS fetcher instance
    fetchbryce = RssFetcher()
    info = TickerToInfo()
    fetchbryce.fetch_from_feed(info, max_to_fetch=500)
	
    with open("../tickers.txt") as tickers:
        # go through each ticker in the s&p 500
        for ticker in tickers:
            # parse endlines from tickers
            ticker = ticker.strip()
            
            # get current stock price
            ticker_price = Stock(ticker).get_price()

            # datavide headlines
            headlines = datavide.datavide_headlines(ticker)
            
            # RSS article headlines
            try:
                rss_headlines = info.get_titles_for_ticker(ticker)
                # print(type(rss_headlines))
                # exit(1)
            except:
                pass

            # calculate average sentiment score for the article headlines of the given ticker
            ticker_sentiment = 0
            ticker_sentiment = get_average_sentiment(headlines)
            print(ticker + " " + str(ticker_sentiment))

            # set number of shares
            num_shares = 0

            # capitalization
            ticker_cap = 0
            
            # if ticker sentiment is greater than 0, we will want to put this stock in our portfolio
            if ticker_sentiment > 0:
                # set number of shares
                num_shares = 5

                # capitalization
                ticker_cap = num_shares * ticker_price
                total_value += ticker_cap
                total_sentiment += ticker_sentiment
                num_invested += 1

            # insert into the database, we will still put assets into the database we do not have positions in
            query_string = "insert into assets values('{}', {}, {}, {})".format(ticker, ticker_sentiment, ticker_price, num_shares)
            c.execute(query_string)
            conn.commit()

    # update our overview table
    current_time = str(datetime.today())
    current_value = total_value
    current_sentiment = total_sentiment / num_invested
    open_value = current_value
    open_sentiment = current_sentiment
    value_change = 0
    sentiment_change = 0
    
    # this will set up the history table
    history_query = "insert into history values('{}', {}, {}, {}, {}, {}, {}, {})".format(current_time, current_value, current_value, current_sentiment, current_sentiment, 0, 0, num_invested)
    c.execute(history_query)
    conn.commit()

    print(total_value)
    conn.close()


# if __name__ == "__main__":
#    # update_portfolio()
#     initialize_portfolio()


