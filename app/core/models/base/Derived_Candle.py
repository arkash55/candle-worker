


from abc import ABC
from app.core.models.base import BaseCandle


class DerivedCandle(BaseCandle, ABC):
    



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
        aligned_timestamp = cls._aligned_timestamp(candles[0].timestamp)
        derived_candle = cls(symbol, aligned_timestamp, True)
        
        derived_candle_attr = cls.get_data_from_aggregated_candles(candles)
        derived_candle._apply_attr(derived_candle_attr)
 

        
        return derived_candle
        


    

    @classmethod
    def start_new(cls, candle):
        """
            Creates a 1 minute candle from a single trade

            Assumptions:
                - Input candle is valid and complete

            Returns:
                - A fully populated, time aligned, but not finalised 1 minute candle
        """

        derived_candle = cls(
            symbol=candle.symbol, 
            timestamp=cls._aligned_timestamp(),
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




    def update(self, candle):
        """
            Updates the current candle using smaller candles

            Assumptions: 
                - The new candle parameter is a candle that exists after the previous
                    smaller candle. (1m candles are updated in order)
                - Candle_1s exists in the correct time window as our current        
                - Candle_1s is finalised


            Raises:
                - Runtime Error: 
                    if the input candle is not finalised
                    if the updated candle is finalised
                    if the input candle does not match window of the current candle
                    
        """

        if self.finalised:
            raise RuntimeError('Cannot update a finalised candle')
        elif not candle.finalised:
              raise RuntimeError('Cannot update a derived candle with an unfinalised candle')
        if not self.timestamp <= candle.timestamp < self.end_timestamp:
            raise RuntimeError('Trade timestamp exists outside candles time window')


        self._high = max(self.high, candle.high)
        self._low = min(self.low, candle.low)
        self._close = candle.close

        self._volume += candle.volume
        self._trade_cnt += candle.trade_cnt
        self._vwap_numerator += candle.vwap_numerator
        self._vwap = self.vwap_numerator / self.volume



    