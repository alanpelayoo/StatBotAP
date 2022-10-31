"""
API Documentation
https://bybit-exchange.github.io/docs/usdc/perpetual/#t-introduction
we have to hide api keys***
"""

#API Imports
from pybit.usdt_perpetual import HTTP
from dotenv import load_dotenv
import os

#Config
mode = "test"
timeframe = 60 #1 hour
kline_limit = 200
z_score_widow = 21



load_dotenv()
api_key_testnet = os.environ["api_key_testnet"]
api_secret_testnet = os.environ["api_secret_testnet"]

api_key_mainnet = os.environ["api_key_mainnet"]
api_secret_mainnet = os.environ["api_secret_mainnet"]


#SELECTED API 
api_key = api_key_testnet if mode == "test" else api_key_mainnet

api_sectret = api_key_testnet if mode == "test" else api_secret_mainnet

#SELECTED URL
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

#SESSION ACTIVATION
session = HTTP(api_url)