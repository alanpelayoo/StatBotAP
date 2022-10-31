"""
    Get symbols info that are trading in Bybit USDT Perpetual
    Returns a large list of symbols with info.w,
"""

import sys
sys.path.append('/Users/alanpelayozepeda/Desktop/apcodes/Python/Finance/StatBotAPcodes/Strat/configuration')

from config_bybit import session, timeframe, kline_limit

def get_tradeable_symbols():
    sym_list = []
    symbols = session.query_symbol()
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
    
    for symbol in symbols:
        if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading":
            sym_list.append(symbol)
    return sym_list

