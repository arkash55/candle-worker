from datetime import timedelta
from app.core.models.base import BaseCandle





class Candle_1m(BaseCandle): 


    _duration: timedelta = timedelta(minutes=1)

    def __init__(self, symbol, timestamp, finalised):
        super().__init__(symbol, timestamp, finalised)


    @classmethod
    def from_past_data(cls, candles):
        """
            Create a 1 minutes candle with 1 second candles within the minute window

            Assumption:
                - All 1 second candles exist within the same minute window
                - All 1 second candles are complete and finalised

        """

        if len(candles) == 0:
            raise ValueError('Past Candle data cannot be empty')
        
        symbol = candles[0].symbol
        aligned_timestamp = candles[0].timestamp.replace(second=0)
        derived_candle = cls(symbol, aligned_timestamp, True)
        
        derived_candle_attr = Candle_1m.get_data_from_aggregated_candles(candles)
        derived_candle._apply_attr(derived_candle_attr)
 

        
        return derived_candle
        


    

    @classmethod
    def start_new(cls, candle):
        derived_candle = cls(
            symbol=candle.symbol, 
            timestamp=candle.timestamp.replace(second=0),
            finalised=False
        )


        derived_candle._open = candle.open
        derived_candle._high = candle.high
        derived_candle._low = candle.low
        derived_candle._close = candle.close

        derived_candle._volume = candle.volume
        derived_candle._vwap = candle.vwap
        derived_candle._vwap_numerator = candle.vwap_numerator
        derived_candle._trade_cnt = candle.trade_cnt
        
        return derived_candle






    @classmethod
    def update(cls, candle):
        pass




