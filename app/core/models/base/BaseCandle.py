

from abc import ABC, abstractmethod
from datetime import timedelta


class BaseCandle(ABC):
    

    _duration: timedelta = None

    def  __init__(self, symbol, timestamp, finalised):

        if self._duration == None:
            raise NotImplementedError(f"{self.__class__.__name__} must define a '_duration' attribute")

        self._symbol = symbol
        self._timestamp = timestamp
        self._finalised = finalised

        self._open = None
        self._close = None
        self._high = None
        self._low = None

        self._trade_cnt = 0
        self._volume = 0
        self._vwap = 0
        self._vwap_numerator = 0 


     # PROPERTIES
    @property
    def symbol(self):
        return self._symbol

    @property
    def open(self):
        return self._open

    @property
    def close(self):
        return self._close
    

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low
    

    @property
    def trade_cnt(self):
        return self._trade_cnt
    

    @property
    def volume(self):
        return self._volume

    @property
    def vwap(self):
        return self._vwap
    

    @property
    def vwap_numerator(self):
        return self._vwap_numerator
    
    
    @property
    def timestamp(self):
        # ensure is aligned
        return self._timestamp
    
    @property
    def finalised(self):
        return self._finalised
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def end_timestamp(self):
        return self.timestamp + self._duration
    

    #STATIC METHODS
    def get_data_from_aggregated_candles(candles):
        sorted_candles = sorted(candles, key=lambda t: t.timestamp)
        
        symbol_ = sorted_candles[0].symbol
        
        open_ = sorted_candles[0].open
        high_ = max(c.high for c in candles)
        low_ = min(c.low for c in candles)
        close_ = sorted_candles[-1].close

        trade_cnt_ = sum(c.trade_cnt for c in candles)
        volume_ = sum(c.volume for c in candles)
        vwap_numerator_ = sum(c.vwap for c in candles)
        vwap_ = vwap_numerator_ / volume_


        return {
            'symbol': symbol_,
            'open': open_,
            'high': high_,
            'low': low_,
            'close': close_, 
            'trade_cnt': trade_cnt_,
            'volume': volume_,
            'vwap_numerator': vwap_numerator_,
            'vwap': vwap_,
        }




    # PUBLIC METHODS
    def finalise(self):
        self._finalised = True


    # INSTANCE METHODS

    def _apply_attr(self, derived_data):
        for key, val in derived_data.items():
            setattr(self, f'_{key}', val)


    # ABSTRACT METHODS

    @classmethod
    @abstractmethod
    def _aligned_timestamp(cls, timestamp=None):
        """
        Creates aligned timestamp for the given timestamp
        Returns:
            datetime
        """
        pass


    @classmethod
    @abstractmethod
    def from_past_data(cls, data):
        pass


    @classmethod
    @abstractmethod
    def start_new(cls, data):
        pass



    @abstractmethod
    def update(self, data):
        pass

