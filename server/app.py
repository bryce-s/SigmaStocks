'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)

##
# API routes
##


@app.route('/api/portfolio')
def portfolio():
    '''Sample API route for data'''
    return jsonify([{'portfolioValue': 100}])


@app.route('/api/stocks')
def getInvestedStocks():
    return jsonify([{'companyName': 'Apple', 'ticker': 'AAPL', 'movement': '+6.03'}, {'companyName': 'Microsoft', 'ticker': 'MSFT', 'movement': '-2.8'}, {'companyName': 'Tesla', 'ticker': 'TSLA', 'movement': '-1.3'}])
##
# View route
##


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    '''Return index.html for all non-api routes'''
    # pylint: disable=unused-argument
    return send_from_directory(app.static_folder, 'index.html')
