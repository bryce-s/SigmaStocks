from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import decimal
import requests
import json
import sqlite3
from iexfinance.stocks import Stock
import datavide
from datetime import date

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
    pass

# function handles the initialization of the portfolio
def initialize_portfolio():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    global starting_wealth
    total_value = 0
    total_sentiment = 0
    num_invested = 0
	
    with open("../tickers.txt") as tickers:
        # go through each ticker in the s&p 500
        for ticker in tickers:
            # parse endlines from tickers
            ticker = ticker.strip()
            
            # get current stock price
            ticker_price = Stock(ticker).get_price()

            # here we will use the api tools to fetch the article headlines for the given ticker
            headlines = datavide.datavide_headlines(ticker)

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
    # current_day
    current_day = date.today()
    current_value = total_value
    current_sentiment = total_sentiment / num_invested
    open_value = current_value
    open_sentiment = current_sentiment
    value_change = 0
    sentiment_change = 0
    overview_query = "insert into overview values({}, {}, {}, {}, {}, {}, {}, {})".format(current_day, current_value, current_sentiment, open_value, open_sentiment, value_change, sentiment_change, num_invested)
    c.execute(overview_query)
    conn.commit()

    print(total_value)
    conn.close()

initialize_portfolio()

test = ["the movie was awesome", "the movie was great!!!!!", "the movie was pretty great and the popcorn was delicious.", "the plot was amazing!!", "the acting rocked. I can't believe the movie was that good"]
# get_average_sentiment(test)
