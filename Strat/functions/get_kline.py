import sys
sys.path.append('..')

from configuration.config_bybit import session, timeframe, kline_limit

import datetime
import time


#Get Start Times
time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)

if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit) 

time_start_seconds = int(time_start_date.timestamp())

#Get historical prices (klines)
def get_price_klines(symbol):
    
    #Get Prices
    prices = session.query_mark_price_kline(
    symbol=symbol,
    interval=timeframe,
    limit=kline_limit,
    from_time=time_start_seconds
    )
    
    time.sleep(0.1)
    if len(prices["result"]) != kline_limit:
        return []
    return prices["result"]