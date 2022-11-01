import json

from .get_kline import get_price_klines
from .get_tradeble_syms import get_tradeable_symbols


def store_price_history(symbols):
    # Get prices and store in dataframe
    counts = 0
    price_history_dict ={}
    for sym in symbols:
        symbol_name = sym["name"]
        price_history = get_price_klines(symbol_name)
        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            counts += 1
            print(f"{counts} items stored")
        else: 
            print(f"{sym} item not stored, not enought len")

    if len(price_history_dict)> 0:
        with open("./data/1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("Prices saved successfully")

def create_new_data():
    print("Connecting to Bybit API and getting symbols...")
    symbols = get_tradeable_symbols()
    if len(symbols)> 0:
        print("Constructing price data to json")
        store_price_history(symbols)
    else:
        print("Query symbols error")