


class Candle_1s():

    

    def __init__(self, symbol, open, close, high, low, trade_cnt, volume, vwap, timestamp, finalised):
        self.__symbol = symbol
        self.__open = open
        self.__close = close
        self.__high = high
        self.__low = low
        self.__trade_cnt = trade_cnt
        self.__volume = volume
        self.__vwap = vwap
        self.__timestamp = timestamp
        self.__finalised = finalised

    # PROPERTIES
    @property
    def symbol(self):
        return self.__symbol

    @property
    def open(self):
        return self.__open

    @property
    def close(self):
        return self.__close
    

    @property
    def high(self):
        return self.__high

    @property
    def low(self):
        return self.__low
    



    @property
    def trade_cnt(self):
        return self.__trade_cnt
    

    @property
    def volume(self):
        return self.__volume

    @property
    def vwap(self):
        return self.__vwap
    
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def finalised(self):
        return self.__finalised
    

    #STATIC METHODS
    @staticmethod
    def _get_ohlc(trades):
        if len(trades) == 0:
            raise ValueError("Cannot build candle from empty trade list")
        
        sorted_trades = sorted(trades, key=lambda t: t.timestamp)
        open_, close_ = sorted_trades[0].price, sorted_trades[-1].price
        high_ = max(t.price for t in sorted_trades)
        low_ = min(t.price for t in sorted_trades)

        return (open_, high_, low_, close_)
        

        

    # METHODS
    @classmethod
    def from_trades(cls, symbol, trades):
        # we need to get open, close, high low
        open_, high_, low_, close_ = cls._get_ohlc(trades)
        volume_ = sum(t.size for t in trades)
        trade_cnt_ = len(trades)
        vwap_ = sum(t.size * t.price for t in trades) / volume_
        candle = cls(
                        symbol=symbol, open=open_, close=close_,
                        high=high_, low=low_, trade_cnt=trade_cnt_,
                        volume=volume_, vwap=vwap_, 
                        timestamp=trades[0].timestamp.replace(microsecond=0), finalised=True
                    )
        return candle







    @classmethod
    def start_new(cls, symbol, timestamp):
        # first trade update will be open
        pass


    def update(self, trade):
        pass 