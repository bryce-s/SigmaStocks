import os
import requests
import json

# function uses datavide api to fetch yahoo finance articles on a given ticker
def datavide_headlines(ticker):
	datavide_key = open("../datavide_key.txt").read()
	api_string = "http://api.datavide.com/api/companies/headlines/{}/week?apikey={}".format(ticker, datavide_key)
	
	data = requests.get(api_string)
	data = data.json()

	headlines = []
	
	for entry in data["data"]:
		headlines.append(entry["headline"])
	
	return(headlines)

headlines = datavide_headlines("MMM")
print(headlines)