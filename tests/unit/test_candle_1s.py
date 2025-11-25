import unittest
from random import randint
from datetime import datetime, timedelta
from app.core.models import Candle_1s, Trade


class Test_Candle_1s(unittest.TestCase):
    


    # def test_upper(self):
        # self.assertEqual('foo'.upper(), 'FOO')


    symbol = 'AAPL'

    def generate_from_trades_data(self, open_, high_, low_, close_, size_):
        trades = []
        curr_time = datetime.now()
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


        

    def test_valid_from_trades(self):
        open_, close_, low_, high_, size_ = 5, 10, 4, 12, 10
        trades = self.generate_from_trades_data(open_=open_, high_=high_, close_=close_, low_=low_, size_=size_)
        candle = Candle_1s.from_trades(symbol=self.symbol, trades=trades)
        vwap_numerator = sum(t.price * t.size for t in trades)
        volume = sum(t.size for t in trades)
        self.assertEqual(candle.open, open_)
        self.assertEqual(candle.close, close_)
        self.assertEqual(candle.low, low_)
        self.assertEqual(candle.high, high_)
        self.assertEqual(candle.timestamp, trades[0].timestamp.replace(microsecond=0))
        self.assertTrue(candle.finalised)
        self.assertEqual(candle.trade_cnt, len(trades))
        self.assertEqual(candle.volume, volume)
        self.assertEqual(candle.vwap, vwap_numerator/volume)


    def test_empty_from_trades(self):
        with self.assertRaises(ValueError):
            Candle_1s.from_trades(self.symbol, [])
        


    def test_start_new(self):
        # our worker should provide an aligned timestamp
        timestamp = datetime.now()
        price, size = 50, 10
        trade = Trade(symbol=self.symbol, price=price, size=size, timestamp= timestamp)
        candle = Candle_1s.start_new(trade=trade)
        self.assertEqual(candle.open, price)
        self.assertEqual(candle.close, price)
        self.assertEqual(candle.low, price)
        self.assertEqual(candle.high, price)
        self.assertEqual(candle.timestamp, timestamp.replace(microsecond=0))
        self.assertEqual(candle.trade_cnt, 1)
        self.assertEqual(candle.volume, size)
        self.assertEqual(candle.vwap, price)
        self.assertFalse(candle.finalised)






