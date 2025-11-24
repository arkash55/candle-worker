import unittest
from datetime import datetime, timedelta
from app.core.models import Candle_1s, Trade


class Test_Candle_1s(unittest.TestCase):
    


    # def test_upper(self):
        # self.assertEqual('foo'.upper(), 'FOO')


    symbol = 'AAPL'

    def generate_trades(self, open_, high_, low_, close_):
        trades = []
        sz = 5
        curr_time = datetime.now()
        trades.append(Trade(self.symbol, high_, sz, curr_time + timedelta(milliseconds=20)))
        trades.append(Trade(self.symbol, close_, sz, curr_time + timedelta(milliseconds=60)))
        trades.append(Trade(self.symbol, open_, sz, curr_time))
        trades.append(Trade(self.symbol, low_, sz, curr_time + timedelta(milliseconds=40)))
        return trades;


        

    def test_valid_from_trades(self):
        open_, close_, low_, high_ = 5, 10, 4, 12
        trades = self.generate_trades(open_=open_, high_=high_, close_=close_, low_=low_)
        candle = Candle_1s.from_trades(self.symbol, trades)
        self.assertEqual(candle.open, open_)
        self.assertEqual(candle.close, close_)
        self.assertEqual(candle.low, low_)
        self.assertEqual(candle.high, high_)


    def test_empty_from_trades(self):
        with self.assertRaises(ValueError):
            Candle_1s.from_trades(self.symbol, [])
        








