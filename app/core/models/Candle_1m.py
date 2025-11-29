from datetime import datetime, timedelta
from app.core.models.base import BaseCandle, Derived_Candle






class Candle_1m(Derived_Candle): 


    _duration: timedelta = timedelta(minutes=1)

    def __init__(self, symbol, timestamp, finalised):
        super().__init__(symbol, timestamp, finalised)


    @classmethod
    def _aligned_timestamp(cls, timestamp=datetime.now()):
        return timestamp.replace(second=0, microsecond=0)    

