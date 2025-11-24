


class Candle_1s():

    

    def __init__(self, symbol, open, close, high, low):
        self.__symbol = symbol
        self.__open = open
        self.__close = close
        self.__high = high
        self.__low = low

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
    

    #static methods
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
        candle = cls(symbol=symbol, open=open_, close=close_, high=high_, low=low_)
        return candle







    @classmethod
    def start_new(cls, symbol, timestamp):
        # first trade update will be open
        pass


    def update(self, trade):
        pass 