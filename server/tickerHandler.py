from urllib.request import urlopen


class Ticker:
    def __init__(self, exchangeList=["NASDAQ", "NYSE", "AMEX"], debug=False):
        self.ticker_dict = self.create_ticker_dict(exchangeList, debug)

    # Input: Company name (str)
    # Output: Ticker (str)
    def get_ticker(self, company_name: str):
        assert isinstance(company_name, str)
        for ticker, name in self.ticker_dict.items():
            if company_name in name:
                return ticker
            else:
                return None

    # Input: Ticker (str)
    # Output: Company name (str)
    def get_company_name(self, ticker: str):
        assert isinstance(ticker, str)
        try:
            return self.ticker_dict[ticker]
        except BaseException:
            return None

    # Input: List of exchanges, debug option
    # Output: dictionary with {ticker, company_name} pairs
    def create_ticker_dict(self, exchangeList, debug):
        assert isinstance(exchangeList, list)
        assert isinstance(debug, bool)
        ticker_dict = {}
        for exchange in ["NASDAQ", "NYSE", "AMEX"]:
            url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
            try:
                if debug:
                    print("Downloading tickers from {}...".format(exchange))
                response = urlopen(url + exchange + '&render=download')
                content = response.read().decode('utf-8').split('\n')
                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0 or len(line) != 9:
                        continue
                    if line[0] not in ticker_dict.keys():
                        ticker_dict[line[0]] = line[1]
                break
            except BaseException:
                continue
        return ticker_dict

# if __name__ == "__main__":
#     g = Ticker()
#     print(g.ticker_dict)
#     print(g.get_ticker('Alphabet'))
#     print(g.get_company_name('AAPL'))
#     # print(get_tickers())
