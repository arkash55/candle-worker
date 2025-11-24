


class Candle_1s():

    

    def __init__(self, open, close, high, low):
        self.__open = open
        self.__close = close
        self.__high = high
        self.__low = low

    # PROPERTIES
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
    

    #static methods
    def get_ohlc(trades):
        if len(trades) == 0:
            return None
        
        sorted_trades = sorted(trades, key=lambda t: t.timestamp)
        open, close = sorted_trades[0].price, sorted_trades[-1].price
        high = max(t.price for t in sorted_trades)
        low = min(t.price for t in sorted_trades)

        return open, high, low, close
        

        

    # METHODS

    
    @classmethod
    def from_trades(cls, symbol, trades):
        # we need to get open, close, high low
        open, high, low, close = cls.get_ohlc(trades)
        candle = Candle_1s(open=open, close=close, high=high, low=low)
        return candle







    @classmethod
    def start_new(cls, symbol, timestamp):
        # first trade update will be open
        pass


    def update(self, trade):
        pass 