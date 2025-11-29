from datetime import datetime, timedelta
from app.core.models import Candle_1m, Candle_1s, Trade
 
 

# 4 trades in this 1 second candle, 100 -> 99 -> 101 -> 99 (each quantity is 3)

def create_single_1s_candle_with_1_trade_and_volume(symbol, timestamp, price):
    candle = Candle_1s.__new__(Candle_1s)

    candle._symbol = symbol
    candle._timestamp = timestamp.replace(microsecond=0)
    candle._finalised = False

    candle._open = price
    candle._high = price
    candle._low = price
    candle._close = price

    candle._volume = 1
    candle._vwap = price
    candle._vwap_numerator = price
    candle._trade_cnt = 1
    return candle



def arith_sum(x):
    return (x * (x+1))/2


def sum_between(first, last):
    cnt = last - first + 1
    return cnt * ((first + last) / 2)


"""

so now we have have count candles
open = price,
low = price,
high = price + (count-1)
close = price + (count-1)
trade_cnt = count
volume = count

// arithmetic sum = (close * (close+1))/2 - ((open-1) * ((open-1)+1))/2
vwap_numerator = arithSum(close) - arithSum(open-1)
vwap = vwap_numerator / (count)



"""



def generate_multiple_1s_candle_with_1_trade_and_volume(symbol, price, count):
    #TODO: ensure we dont pass 60 seconds !!!!!
    aligned_timestamp = datetime.now().replace(second=0)
    candles = []

    for i in range(count):
        candles.append(
            create_single_1s_candle_with_1_trade_and_volume(
                symbol,
                aligned_timestamp + timedelta(seconds=i%60),
                price + i
            )
        )
        
    return candles
    




