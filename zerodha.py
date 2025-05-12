import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect


class Holding:
    def __init__(self, ticker: str, qty: int, avg_price: float):
        self.ticker = ticker
        self.qty = qty
        self.avg_price = avg_price


load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
REQUEST_TOKEN = os.getenv("REQUEST_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=API_KEY)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

# data = kite.generate_session(REQUEST_TOKEN, api_secret=SECRET_KEY)
kite.set_access_token(ACCESS_TOKEN)


def getCurrentHoldings() -> list[Holding]:
    holdings = kite.holdings()

    portfolio = [
        Holding(x["tradingsymbol"], x["quantity"], x["average_price"]) for x in holdings
    ]  # type: ignore
    return portfolio
