import requests
import json
import datetime
import calendar
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import decimal
import matplotlib.pyplot as plt
import math

# function handles computing the correlation coefficient between the sentiment score and stock prices
def compute_correlation(sentiments, prices):
	# sentiment magnitude
	sent_mag = 0
	for sent in sentiments:
		sent_mag += (sent * sent)
	
	# prices magnitude
	price_mag = 0
	for price in prices:
		price_mag += (price * price)

	# dot product
	prod = 0
	for i in range(len(sentiments)):
		prod += (sentiments[i] * prices[i])

	# correlation coefficients
	corr_coef = prod / (math.sqrt(sent_mag * price_mag))

	return(corr_coef)

# function handles taking headline and returning sentiment score
def get_average_sentiment(input_list):
    sia = SentimentIntensityAnalyzer()
    total = 0.0
    size = len(input_list)

    for headline in input_list:
        intensity = sia.polarity_scores(headline)
        score = intensity["compound"]
        total += score

    if size > 0:
        average = total / size
        return(average)
    else:
        return(0)

def main():
	stocknews_key = "mzwgkanip8iidvqxjxm4hxoav88sakezfvuf84oz"
	tiingo_key = "460f9672dc0ceb075f798235a3793e253a80af8e"

	ticker = input("Enter ticker: ")
	ticker = ticker.upper()
	api_string = "https://stocknewsapi.com/api/v1?tickers={}&items={}&token={}".format(ticker, 50, stocknews_key)

	past_headlines = requests.get(api_string)
	past_headlines = past_headlines.json()
	
	date_headlines = {}
	dates = []
	
	# parse dates and headlines from the stocknews api
	for entry in past_headlines["data"]:
		# parse and setup date
		article_date = entry["date"]
		date = article_date.split()
		day = date[1]
		month = str(list(calendar.month_abbr).index(date[2]))
		year = date[3]
		final_date = year + "-" + month + "-" + day

		if final_date not in dates:
			dates.append(final_date)

		# get stock headline
		headline = entry["title"]
		if final_date in date_headlines:
			date_headlines[final_date].append(headline)
		else:
			date_headlines[final_date] = []
			date_headlines[final_date].append(headline)

	# order the dates in ascending order
	dates.sort()
	# print(dates)
	# exit(1)

	prices = []
	sentiments = []

	for date in dates:
		tiingo_str = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&token={}".format(ticker, date, date, tiingo_key)
		try:
			current_price = requests.get(tiingo_str).json()[0]["close"]
		except:
			current_price = prices[-1]
		
		current_sentiment = get_average_sentiment(date_headlines[date])

		prices.append(current_price)
		sentiments.append(current_sentiment)
	
	# plot
	plt.subplot("211")
	plt.plot(prices, "b")
	plt.xticks(range(len(dates)), dates)
	plt.xlabel("Day")
	plt.ylabel("Price")
	plt.title(ticker + " Stock Price")
	plt.subplots_adjust(hspace=0.50)

	plt.subplot("212")
	plt.plot(sentiments, "r")
	plt.xticks(range(len(dates)), dates)
	plt.xlabel("Day")
	plt.ylabel("Sentiment")
	plt.title(ticker + " Sentiment Score")
	plt.show()

	# print the correlation coefficient
	corr_coef = compute_correlation(sentiments, prices)
	print("correlation coefficient = " + str(corr_coef))
	
if __name__ == "__main__":
	main()