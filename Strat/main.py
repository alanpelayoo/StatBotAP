
import json
from functions.store_prices import create_new_data
from functions.cointegration import get_cointegrated_pairs 

if __name__ == "__main__":
    print("Starting bot...")

    #Flags to call functions
    new_data = False

    if new_data:
        create_new_data()
    
    with open("data/1_price_list.json") as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            coint_pairs = get_cointegrated_pairs(price_data)
    print("done")
        