from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import decimal
import requests
import json
import sqlite3
from iexfinance.stocks import Stock

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

    average = round(total / size, 8)
    print(average)

# function handles updating the portfolio by retrieving new articles, recalculating sentiment, and changing position
def update_portfolio():
    pass

# function handles the initialization of the portfolio
def initialize_portfolio():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    global starting_wealth
    total_value = 0
	
    with open("../tickers.txt") as tickers:
        # go through each ticker in the s&p 500
        for ticker in tickers:
            ticker = ticker.strip()

            # here we will use the custom api tool to fetch the articles for the given ticker

            # calculate average sentiment score for the articles of the given ticker
            # ticker_sentiment = get_average_sentiment()
            ticker_sentiment = 1

            if ticker_sentiment > 0:
                # get current stock price
                ticker_price = Stock(ticker).get_price()
                total_value += ticker_price
                print(ticker + " " + str(ticker_price))

                # set number of shares
                num_shares = 5

                # capitalization
                ticker_cap = num_shares * ticker_price

                # add entry to portfolio database - this is a test
                # query_string = "insert into assets values('{}', {}, {}, {})".format(ticker, ticker_sentiment, ticker_price, num_shares)
                # c.execute(query_string)
                # conn.commit()
                
                # subtract total amount from initial amount
                starting_wealth -= ticker_cap

    print(total_value)
    conn.close()

initialize_portfolio()

test = ["the movie was awesome", "the movie was great!!!!!", "the movie was pretty great and the popcorn was delicious.", "the plot was amazing!!", "the acting rocked. I can't believe the movie was that good"]
# get_average_sentiment(test)
