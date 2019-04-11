#!flask/bin/python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/portfolio', methods=['GET'])
def portfolio():
    '''Sample API route for data'''
    return jsonify([{'portfolioValue': 100}])


@app.route('/api/stocks', methods=['GET'])
def getInvestedStocks():
    stocks = [
        {'companyName': 'Apple', 'ticker': 'AAPL', 'movement': '+6.03'},
        {'companyName': 'Microsoft', 'ticker': 'MSFT', 'movement': '-2.8'},
        {'companyName': 'Tesla', 'ticker': 'TSLA', 'movement': '-1.3'},
        {'companyName': 'Google', 'ticker': 'GOOG', 'movement': '+3.4'}
    ]
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
