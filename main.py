import logging
import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
REQUEST_TOKEN = os.getenv("REQUEST_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=API_KEY)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

# data = kite.generate_session(REQUEST_TOKEN, api_secret=SECRET_KEY)
kite.set_access_token(ACCESS_TOKEN)


# Fetch all orders
holdings = kite.holdings()
portfolio = [x["tradingsymbol"] for x in holdings]
print(portfolio)
