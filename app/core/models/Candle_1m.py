from datetime import datetime, timedelta
from app.core.models.base import BaseCandle, DerivedCandle
# from app.core.models.base.Derived_Candle import DerivedCandle





class Candle_1m(DerivedCandle): 


    _duration: timedelta = timedelta(minutes=1)

    def __init__(self, symbol, timestamp, finalised):
        super().__init__(symbol, timestamp, finalised)


    @classmethod
    def _aligned_timestamp(cls, timestamp=datetime.now()):
        return timestamp.replace(second=0, microsecond=0)    

