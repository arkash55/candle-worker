from datetime import datetime, timedelta

from app.core.models.base import BaseCandle


class Candle_1s(BaseCandle):

    _duration: timedelta = timedelta(seconds=1)

    def __init__(self, symbol, timestamp, finalised):
        super().__init__(symbol=symbol, timestamp=timestamp, finalised=finalised)


    

    #STATIC METHODS MADE FOR FOR_TRADES FACTORY METHOD


    @staticmethod
    def _calc_ohlc(trades):
        """
        Calculates open, high, low and close from a list of historical trades
            - Assumes trades may be unsorted
            - Assume all trades exist within the same 1 second window

        Returns: 
        (open, high, low, close)
        """

        if len(trades) == 0:
            raise ValueError("Cannot build candle from empty trade list")
        
        sorted_trades = sorted(trades, key=lambda t: t.timestamp)
        open_, close_ = sorted_trades[0].price, sorted_trades[-1].price
        high_ = max(t.price for t in sorted_trades)
        low_ = min(t.price for t in sorted_trades)

        return (open_, high_, low_, close_)
        
    @staticmethod
    def _calc_volume(trades):
        return sum(t.size for t in trades)
    
    @staticmethod
    def _calc_vwap_numerator(trades):
        return sum(t.price * t.size for t in trades)



    @staticmethod
    def _calc_vwap(trades):
        vwap_numerator = Candle_1s._calc_vwap_numerator(trades=trades)
        vwap_denominator = sum(t.size for t in trades)
        return vwap_numerator/vwap_denominator

    @staticmethod
    def _calc_trade_cnt(trades):
        return len(trades)

        

    # METHODS


    @classmethod
    def _aligned_timestamp(cls, timestamp=datetime.now()):
        return timestamp.replace(microsecond=0)


    # HUGE ASSUMPTION, ensure all trades are valid, they are of same symbol,and exist in the same candle window!!!! Care when creating this functionality upstream
    
    @classmethod
    def from_past_data(cls, trades):
        """
            Creates a 1 second candle from a list trades

            Assumptions:
                - Trades are all from the same symbol
                - Trades are not missing any data
                - Trades all exist within the same 1 second window

            Returns:
                - A fully populated, finalised and time aligned 1 second candle  

        """

        if len(trades) == 0:
            raise ValueError('Cannot create candle with empty an empty trades list')

        aligned_timestamp = cls._aligned_timestamp(trades[0].timestamp)
        candle = cls(
                        symbol=trades[0].symbol, 
                        timestamp=aligned_timestamp, finalised=True
                    )
        candle._open, candle._high,  candle._low, candle._close = cls._calc_ohlc(trades)

        candle._volume = cls._calc_volume(trades)
        candle._vwap_numerator = cls._calc_vwap_numerator(trades)
        candle._vwap = cls._calc_vwap(trades)
        candle._trade_cnt = cls._calc_trade_cnt(trades)
        
        return candle



    @classmethod
    def start_new(cls, trade):
        """
            Creates a 1 second candle from a single trade

            Assumptions:
                - Trade is not missing any data

            Returns:
                - A fully populated, time aligned, but not finalised 1 second candle
        """

        aligned_timestamp = cls._aligned_timestamp(trade.timestamp)
        candle = cls(symbol=trade.symbol, timestamp=aligned_timestamp, finalised=False)
        candle._open = candle._high = candle._low = candle._close = trade.price
        candle._volume = trade.size
        candle._vwap = trade.price
        candle._vwap_numerator = trade.price * trade.size
        candle._trade_cnt = 1
        return candle



    def update(self, trade):
        """
            Updates the current 1 second candle with the information from the new trade

            Notes:
                - Updates volume, close, high, low, trade_cnt, vwap_numerator and vwap

            Assumptions:
                - Trade is not missing any data
                - Trade belongs to the same symbol
                - Trade belongs to the same time window
                - Candle is not finalised
                    
        """


        if self.finalised:
            raise RuntimeError('Cannot update a finalised candle')
        if not self.timestamp <= trade.timestamp < self.end_timestamp:
            raise RuntimeError('Trade timestamp exists outside candles time window')


        self._close = trade.price
        self._volume += trade.size
        self._high = max(self._high, trade.price)
        self._low = min(self._low, trade.price)
        self._vwap_numerator += trade.price * trade.size
        self._vwap = self._vwap_numerator/self._volume
        self._trade_cnt += 1

    
    
    # Finalises Candle, to be called when the candle window has ended
    def finalise(self):
        self._finalised = True