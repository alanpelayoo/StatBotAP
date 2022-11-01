
import sys
sys.path.append('..')
from configuration.config_bybit import z_score_widow

import math
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import numpy as np 

#Calculate Z score
def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_widow).mean()
    std = df.rolling(center=False, window=z_score_widow).std()
    x = df.rolling(center=False, window=1).mean()
    df["SCORE"] = ( x -mean ) / std
    return df["SCORE"].astype(float).values


# Calculate Spread 
def calculate_spread(series1,series2,hedge_ratio):
    spread = pd.Series(series1) - (pd.Series(series2) * hedge_ratio)
    return spread

#Calculate cointegration
def calulate_cointegration(series1,series2):
    coint_flag = 0
    coint_res = coint(series1,series2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]

    model = sm.OLS(series1,series2).fit()
    hedge_ratio = model.params[0]

    spread = calculate_spread(series1,series2,hedge_ratio)
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])

    if p_value < 0.05 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, round(p_value,2), round(coint_t,2), round(critical_value,2), round(hedge_ratio,2), zero_crossings )

#Put classes into a list
def extract_close_prices(prices):
    close_prices = []
    for prices_value in prices:
        if math.isnan(prices_value["close"]): #Check whether a value is NaN, Not A Number
            return []
        close_prices.append(prices_value["close"])
    return close_prices

#Calculate cointegrated pairs
def get_cointegrated_pairs(prices):
    #Loop through coins and check for co-integration
    coint_pair_list = []
    included_list = []
    count = 0
    for sym_1 in prices.keys():
        for sym_2 in prices.keys():
            if sym_2 != sym_1:
                #Get unique id combinations
                sorted_characters = sorted(sym_1+sym_2)
                unique = "".join(sorted_characters)
                if unique in included_list:
                    break
                
                #Get Close Prices
                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

                #Check for cointegration
                coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings = calulate_cointegration(series_1,series_2)
                if coint_flag ==1 :
                    included_list.append(unique)
                    coint_pair_list.append({
                        "sym_1": sym_1,
                        "sym_2": sym_2,
                        "p_value": p_value,
                        "t_value": t_value,
                        "c_value": c_value,
                        "hede_ratio": hedge_ratio,
                        "zero_crossings": zero_crossings
                    })

    df_coint = pd.DataFrame(coint_pair_list)
    df_coint = df_coint.sort_values("zero_crossings",ascending=False)
    df_coint.to_csv("data/2_cointegrated_pairs.csv")
    return df_coint