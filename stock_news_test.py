import os
import requests
import json

def main():
	api_key = open("stocknews_key.txt", "r").read()
	ticker = input("Enter ticker ")
	api_string = "https://stocknewsapi.com/api/v1?tickers={}&items={}&token={}".format(ticker, 50, api_key)

	data = requests.get(api_string)
	data = data.json()

	json_string = json.dumps(data, sort_keys=True, indent=4)
	print(json_string)

if __name__ == "__main__":
	main()