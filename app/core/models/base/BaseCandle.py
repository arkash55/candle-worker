

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
    



    # ABSTRACT METHODS
    @classmethod
    @abstractmethod
    def start_new(cls, source):
        pass



    @abstractmethod
    def update(self, source):
        pass


    # PUBLIC METHODS
    def finalise(self):
        self._finalised = True
