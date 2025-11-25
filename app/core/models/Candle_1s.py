from datetime import timedelta


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
        self.__vwap_numerator = vwap * volume


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
    
    @property
    def end_timestamp(self):
        return self.__timestamp + timedelta(seconds=1)
    

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
        
    @staticmethod
    def _get_volume(trades):
        return sum(t.size for t in trades)

    @staticmethod
    def _get_vwap(trades):
        vwap_numerator = sum(t.price * t.size for t in trades)
        vwap_denominator = sum(t.size for t in trades)
        return vwap_numerator/vwap_denominator

    @staticmethod
    def _get_trade_cnt(trades):
        return len(trades)

        

    # METHODS


    # HUGE ASSUMPTION, ensure all trades are valid, they are of same symbol,and exist in the same candle window!!!! Care when creating this functionality upstream

    @classmethod
    def from_trades(cls, symbol, trades):
        open_, high_, low_, close_ = cls._get_ohlc(trades)
        volume_ = cls._get_volume(trades)
        trade_cnt_ = cls._get_trade_cnt(trades)
        vwap_ = cls._get_vwap(trades)
        candle = cls(
                        symbol=symbol, open=open_, close=close_,
                        high=high_, low=low_, trade_cnt=trade_cnt_,
                        volume=volume_, vwap=vwap_, 
                        timestamp=trades[0].timestamp.replace(microsecond=0), finalised=True
                    )
        return candle



    @classmethod
    def start_new(cls, trade):
        open_ = high_ = low_ = close_ = trade.price
        volume_, trade_cnt_, vwap_ = trade.size, 1, trade.price
        aligned_timestamp = trade.timestamp.replace(microsecond=0)
        candle = cls(
                        symbol=trade.symbol, open=open_, close=close_,
                        high=high_, low=low_, trade_cnt=trade_cnt_,
                        volume=volume_, vwap=vwap_, 
                        timestamp=aligned_timestamp, finalised=False
                    )
        return candle



    def update(self, trade):
        if self.finalised:
            raise RuntimeError('Cannot update a finalised candle')
        if not self.timestamp <= trade.timestamp < self.end_timestamp:
            raise RuntimeError('Trade timestamp exists outside candles time window')


        self.__close = trade.price
        self.__volume += trade.size
        self.__high = max(self.__high, trade.price)
        self.__low = min(self.__low, trade.price)
        self.__vwap_numerator += trade.price * trade.size
        self.__vwap = self.__vwap_numerator/self.__volume
        self.__trade_cnt += 1

    def finalise(self):
        self.__finalised = True