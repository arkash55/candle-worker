import unittest
from datetime import datetime
from app.core.models import Candle_1s, Trade


class Test_Candle_1s(unittest.TestCase):
    


    # def test_upper(self):
        # self.assertEqual('foo'.upper(), 'FOO')


    symbol = 'AAPL'

    def generate_trades(self, open, close, low, high):
        trades = []
        sz = 5;
        trades.append(Trade(self.symbol, open, sz, datetime.now()))
        trades.append(Trade(self.symbol, low, sz, datetime.now()))
        trades.append(Trade(self.symbol, high, sz, datetime.now()))
        trades.append(Trade(self.symbol, close, sz, datetime.now()))
        return trades;


        

    def test_from_trades(self):
        open, close, low, high = 5, 10, 4, 12
        trades = self.generate_trades(open=open, close=close, low=low, high=high)
        candle = Candle_1s.from_trades(self.symbol, trades)
        self.assertEqual(candle.open, open)
        self.assertEqual(candle.close, close)
        self.assertEqual(candle.low, low)
        self.assertEqual(candle.high, high)









