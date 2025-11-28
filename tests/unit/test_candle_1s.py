import unittest
from random import randint, random
from datetime import datetime, timedelta
from app.core.models import Candle_1s, Trade


class Test_Candle_1s(unittest.TestCase):


    symbol = 'AAPL'

    def generate_from_trades_data(self, open_, high_, low_, close_, size_):
        trades = []
        curr_time = datetime.now().replace(microsecond=0)
        trades.append(Trade(
                symbol=self.symbol, price=high_,
                size=size_, timestamp=curr_time + timedelta(milliseconds=20),
            ))
        trades.append(Trade(
                symbol=self.symbol, price=close_,
                size=size_, timestamp=curr_time + timedelta(milliseconds=60),
            ))
        trades.append(Trade(
                symbol=self.symbol, price=open_,
                size=size_, timestamp=curr_time,
            ))
        trades.append(Trade(
                symbol=self.symbol, price=low_,
                size=size_, timestamp=curr_time + timedelta(milliseconds=40),
            ))
        return trades;



    def assert_candle_equal(self, candle, open, high, low, close, trade_cnt, volume, vwap, timestamp, is_finalised, almost_equal_vwap):
        self.assertEqual(candle.open, open)
        self.assertEqual(candle.high, high)
        self.assertEqual(candle.low, low)
        self.assertEqual(candle.close, close)

        self.assertEqual(candle.trade_cnt, trade_cnt)
        self.assertEqual(candle.volume, volume)

        self.assertEqual(candle.timestamp, timestamp)
        

        assert_finalised_fn = self.assertTrue if is_finalised else self.assertFalse
        assert_finalised_fn(candle.finalised)

        assert_vwap_fn = self.assertAlmostEqual if almost_equal_vwap else self.assertEqual
        assert_vwap_fn(candle.vwap, vwap)







        

    def test_valid_from_trades(self):
        """
            Ensures from_trades() returns a candle with correctly caluculates attributes 
        """

        open_, close_, low_, high_, size_ = 5, 10, 4, 12, 10
        trades = self.generate_from_trades_data(open_=open_, high_=high_, close_=close_, low_=low_, size_=size_)
        candle = Candle_1s.from_trades(trades=trades)
        vwap_numerator = sum(t.price * t.size for t in trades)
        volume = sum(t.size for t in trades)

        self.assert_candle_equal(
            candle=candle,
            open=open_,
            high=high_, 
            low=low_,
            close=close_,
            trade_cnt=len(trades),
            volume=volume,
            vwap=vwap_numerator/volume,
            timestamp=trades[0].timestamp.replace(microsecond=0),
            is_finalised=True,
            almost_equal_vwap=False
        )

    




    def test_empty_from_trades(self):
        """
            Ensures from_trades() handles empty input list
        """

        with self.assertRaises(ValueError):
            Candle_1s.from_trades([])
        


    def test_start_new(self):
        """
            Ensures we can create a new candle with correct attributes from a single trade            
        """


        timestamp = datetime.now()
        price, size = 50, 10
        trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=trade)

        self.assert_candle_equal(
            candle=candle,
            open=price,
            high=price, 
            low=price,
            close=price,
            trade_cnt=1,
            volume=size,
            vwap=price,
            timestamp=timestamp.replace(microsecond=0),
            is_finalised=False,
            almost_equal_vwap=False
        )


  


    def test_update(self):
        """
            Tests candle updates with a new trade correctly
        """

        last_price, last_size, last_timestamp = 50, 10, datetime.now().replace(microsecond=0)
        latest_price, latest_size, latest_timestamp = 55, 20, last_timestamp+timedelta(milliseconds=20) 
        last_trade = Trade(symbol=self.symbol, price=last_price, size=last_size, 
        timestamp=last_timestamp)
        latest_trade = Trade(symbol=self.symbol, price=latest_price, size=latest_size, timestamp=latest_timestamp)
        candle = Candle_1s.start_new(trade=last_trade)
        candle.update(latest_trade)
        latest_vwap_numerator = last_trade.price * last_trade.size + latest_trade.price * latest_trade.size
        latest_vwap_denominator = last_trade.size + latest_trade.size


        self.assert_candle_equal(
            candle=candle,
            open=last_trade.price,
            high=latest_trade.price, 
            low=last_trade.price,
            close=latest_trade.price,
            trade_cnt=2,
            volume=last_trade.size + latest_trade.size,
            vwap=latest_vwap_numerator/latest_vwap_denominator,
            timestamp=last_trade.timestamp,
            is_finalised=False,
            almost_equal_vwap=False
        )

        



    # required for testing vwap (numerator -> vwap), volume, trade_cnt accumulation
    def test_multiple_updates(self):
        """
            Tests candle accumulates and updates with multiple new trades correctly
        """

        aligned_timestamp = datetime.now().replace(microsecond=0)
        trade_cnt = 10
        prices = [random()*100 for _ in range(trade_cnt)]
        sizes = [randint(1, 150) for _ in range(trade_cnt)]
        trades = [
                    Trade(self.symbol, price=prices[i], size=sizes[i], timestamp=aligned_timestamp+timedelta(microseconds=i)) 
                    for i in range(trade_cnt)
                ]
        candle = Candle_1s.start_new(trades[0])
        
        for i in range(1, trade_cnt):
            candle.update(trades[i])



        pred_open = trades[0].price
        pred_high = max(prices)
        pred_low = min(prices)
        pred_close = trades[-1].price

        pred_vwap_numerator = sum(prices[i] * sizes[i] for i in range(trade_cnt))
        pred_vwap_denominator = sum(sizes)
        pred_volume = pred_vwap_denominator

        pred_timestamp = trades[0].timestamp.replace(microsecond=0)


        self.assert_candle_equal(
            candle=candle,
            open=pred_open,
            high=pred_high, 
            low=pred_low,
            close=pred_close,
            trade_cnt=trade_cnt,
            volume=pred_volume,
            vwap=pred_vwap_numerator/pred_vwap_denominator,
            timestamp=pred_timestamp,
            is_finalised=False,
            almost_equal_vwap=True
        )

        




    def test_failed_update_on_finalised_candle(self):
        """
            Ensures candle cannot be updated if finalised
        """
        timestamp = datetime.now().replace(microsecond=0)
        price, size = 50, 10
        last_trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=last_trade)
        latest_trade = Trade(symbol=self.symbol, price=price+1, size=size+5, timestamp= timestamp+timedelta(microseconds=50))
        candle.finalise()

        with self.assertRaises(RuntimeError):
            candle.update(latest_trade)



    def test_failed_trade_before_candle_window(self):

        """
            Ensures candle cannot be updated with a trade before it's window
        """

        timestamp = datetime.now().replace(microsecond=0)
        price, size = 50, 10
        last_trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=last_trade)
        latest_trade = Trade(symbol=self.symbol, price=price+1, size=size+5, timestamp= timestamp-timedelta(seconds=2))

        with self.assertRaises(RuntimeError):
            candle.update(latest_trade)



    def test_failed_update_trade_after_candle_window(self):

        """
            Ensures candle cannot be updated with a trade after it's window
        """

        timestamp = datetime.now().replace(microsecond=0)
        price, size = 50, 10
        last_trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=last_trade)
        latest_trade = Trade(symbol=self.symbol, price=price+1, size=size+5, timestamp= timestamp+timedelta(seconds=2))

        with self.assertRaises(RuntimeError):
            candle.update(latest_trade)


    def test_failed_update_trade_on_candle_window_close(self):

        """
            Ensures candle cannot be updated with a trade on it's window close
        """

        timestamp = datetime.now().replace(microsecond=0)
        price, size = 50, 10
        last_trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=last_trade)
        latest_trade = Trade(symbol=self.symbol, price=price+1, size=size+5, timestamp= timestamp+timedelta(seconds=1))

        with self.assertRaises(RuntimeError):
            candle.update(latest_trade)


