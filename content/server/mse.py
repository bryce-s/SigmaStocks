import prediction
import csv
import requests
import json
import datetime

# function returns the stock price for a given day
def get_price(ticker, date):
	tiingo_key = "57fd850b2fc893255eec40ea1815a5931dba6f06"

	current_price = 0
	try:
		tiingo_str = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&token={}".format(ticker, date, date, tiingo_key)
		current_price = float(requests.get(tiingo_str).json()[0]["close"])
	except:
		pass
	
	return(current_price)

def main():
	reader = csv.DictReader(open('../data/sorted_news.csv'))
	next(reader)

	# statistics
	mse = 0
	correct_trend = 0
	wrong_trend = 0

	total_tested = 0
	counter = 0

	for row in reader:
		counter += 1
		
		# get the stock
		stock = row["ticker"]
		
		# extracting date information
		date_str = row["date"]
		year_str = date_str[0:4]
		year = int(year_str)
		month_str = date_str[4:6]
		month = int(month_str)
		day_str = date_str[6:8]
		day = int(day_str)

		current_date = datetime.datetime(year=year, month=month, day=day)
		currentdate_str = str(current_date).split()[0]
		
		next_date = current_date + datetime.timedelta(days=1)
		nextdate_str = str(next_date).split()[0]

		try:
			# get the current day stock price
			current_price = get_price(stock, currentdate_str)
			
			# get the regression prediction
			pred, regression_pred = prediction.predict_pair(stock, 1, current_date)

			# grab the actual next day price
			nextday_price = get_price(stock, nextdate_str)
			
			# compute the MSE
			if nextday_price != 0:
				mse += (nextday_price - regression_pred[0]) * (nextday_price - regression_pred)
				total_tested += 1

				# determine if the trend was correctly forecasted
				if (regression_pred[0] > current_price) and (nextday_price > current_price):
					correct_trend += 1
				elif (regression_pred[0] < current_price) and (nextday_price < current_price):
					correct_trend += 1
				else:
					wrong_trend +=1 
		except:
			pass
		
		if counter > 1000:
			break
	
	# output the statistics
	final_mse = mse / total_tested
	correct = correct_trend / total_tested
	wrong = wrong_trend / total_tested
	print("mean squared error = " + str(final_mse))
	print("percent trend correct = " + str(correct))
	print("percent trend wrong = " + str(wrong))

if __name__ == "__main__":
	main()