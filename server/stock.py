
from datetime import datetime, timedelta
from iexfinance.stocks import Stock, get_historical_data

# https://addisonlynch.github.io/iexfinance/devel/stocks.html


class Stock_Obj:
    def __init__(self, ticker: str):
        self.ticker = ticker

    # Input: None
    # Output: current price
    def get_current_value(self):
        return Stock(self.ticker).get_price()

    # Input: Date
    # Output: Stock movement for Date - 1 Day
    def get_prev_day_movement(self, date=datetime.today().date()):
        end = date - timedelta(days=1)
        prev_val = get_historical_data(self.ticker, end, date)[
            str(end)]['open']
        return round(((self.get_current_value() - prev_val) / prev_val), 4)

    # Input: Date, Delta
    # Output: Movement from Date - 1 to Date
    def get_delta_calculation(self, date=datetime.today(), delta=24):
        end = date + timedelta(hours=delta)
        historical_data = get_historical_data(self.ticker, date, end)
        return round((historical_data[str(
            end.date())]['open'] - historical_data[str(date.date())]['open']), 4)


# if __name__ == '__main__':
    # t = Stock_Obj('AAPL')
    # print(t.get_prev_day_movement())
    # print(t.get_quote()['latestPrice'])
    # print(t.get_current_value())
    # print(t.get_delta_calculation())
