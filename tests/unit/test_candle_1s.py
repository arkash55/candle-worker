import unittest

from app.core.models import Candle_1s


class Test_Candle_1s(unittest.TestCase):
    


    # def test_upper(self):
        # self.assertEqual('foo'.upper(), 'FOO')

    def test_from_trades(self):
        candle = Candle_1s.from_trades('abs', 4)
        self.assertTrue(candle)






