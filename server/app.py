#!flask/bin/python
from flask import Flask, jsonify
from flask_cors import CORS
from time import sleep
import sys
import threading
import sqlite3
from analyzer import update_portfolio


app = Flask(__name__)

CORS(app)



@app.route('/')
def index():
    return "Hello, World!"



def check_if_portfoilo_inited():
    """return True if portfolio is initted"""
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    try:
        c.execute("select * from assets").fetchall()
    except:
        print('ur portfolio bad')
        # uhh this should kill app.py not thread
        exit(1)


def analyzer_run_wraper():
    with app.app_context():
         while True:
            update_portfolio()            
            sleep(60*60*2) # we refetch every two hours for now.



            

# @app.route('/api/portfolio', methods=['GET'])
# def portfolio():
#     '''Sample API route for data'''
#     return jsonify([{'portfolioValue': 100}])


# @app.route('/api/stocks', methods=['GET'])
# def getInvestedStocks():
#     stocks = [
#         {'companyName': 'Apple', 'ticker': 'AAPL', 'movement': '+6.03'},
#         {'companyName': 'Microsoft', 'ticker': 'MSFT', 'movement': '-2.8'},
#         {'companyName': 'Tesla', 'ticker': 'TSLA', 'movement': '-1.3'},
#         {'companyName': 'Google', 'ticker': 'GOOG', 'movement': '+3.4'}
#     ]
#     return jsonify(stocks)


@app.before_first_request
def init_analysis():
    check_if_portfoilo_inited()
    thread = threading.Thread(target = analyzer_run_wraper)
    thread.start()
    print('portfolio thread runnning!')
    # refresh_time = sys.argv[1]

if __name__ == '__main__':
    app.run()

