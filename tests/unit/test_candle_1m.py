import unittest
from random import randint, random
from datetime import datetime, timedelta
from app.core.models import Candle_1m, Candle_1s, Trade
from tests.utils.candle_factory import create_single_1s_candle_with_1_trade_and_volume, generate_multiple_1s_candle_with_1_trade_and_volume, sum_between


class Test_Candle_1m(unittest.TestCase):


    symbol = 'AAPL'





    def assert_candle_equal(self, candle, open, high, low, close, trade_cnt, volume, vwap, timestamp, is_finalised, almost_equal_vwap, symbol = 'AAPL'):
        self.assertEqual(candle.symbol, symbol)
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





    def test_empty_from_past_data(self):
        """
            Ensures from_past_data() handles empty input list
        """

        with self.assertRaises(ValueError):
            Candle_1m.from_past_data([])
            
        



    def test_valid_from_past_data(self):
        """
            Ensures from_past_data() returns a candle with correctly caluculates attributes 
        """

        open = 100
        cnt = 10
        candles = generate_multiple_1s_candle_with_1_trade_and_volume(self.symbol, open, 10)
        derived_candle = Candle_1m.from_past_data(candles);


        pred_symbol = self.symbol
        pred_open = open
        pred_high = open + cnt - 1
        pred_low = open
        pred_close = open + cnt - 1

        pred_vwap_numerator = sum_between(pred_open, pred_close)
        pred_volume = cnt
        pred_trade_cnt = cnt;
        pred_vwap = pred_vwap_numerator / pred_volume
        pred_timestamp = candles[0].timestamp.replace(second=0)



        self.assert_candle_equal(
            candle=derived_candle,
            symbol=pred_symbol,
            open=pred_open,
            high=pred_high, 
            low=pred_low,
            close=pred_close,
            trade_cnt=pred_trade_cnt,
            volume=pred_volume,
            vwap=pred_vwap,
            timestamp=pred_timestamp,
            is_finalised=True,
            almost_equal_vwap=False
        )

    



    def test_start_new(self):
        """
            Ensures we can create a new candle with correct attributes from a single 1 minute candle       
        """ 

        baseline_timestamp = datetime.now().replace(microsecond=0)
        price = 100
        candle_1s = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp,
            price
        )

        derived_candle = Candle_1m.start_new(candle=candle_1s)


        pred_symbol = self.symbol
        pred_open = price
        pred_high = price
        pred_low = price
        pred_close = price

        pred_vwap_numerator = price
        pred_volume = 1
        pred_trade_cnt = 1;
        pred_vwap = pred_vwap_numerator / pred_volume
        pred_timestamp = baseline_timestamp.replace(second=0)

        self.assert_candle_equal(
            candle=derived_candle,
            symbol=pred_symbol,
            open=pred_open,
            high=pred_high, 
            low=pred_low,
            close=pred_close,
            trade_cnt=pred_trade_cnt,
            volume=pred_volume,
            vwap=pred_vwap,
            timestamp=pred_timestamp,
            is_finalised=False,
            almost_equal_vwap=False
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

        baseline_timestamp = datetime.now().replace(microsecond=0)
        price_1, price_2 = 100, 110
        first_candle_1s_a = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp,
            price_1
        )


        derived_candle = Candle_1m.start_new(candle=first_candle_1s_a)

        new_candle_1s = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            derived_candle.timestamp - timedelta(minutes=2),
            price_2
        )



        with self.assertRaises(RuntimeError):
              derived_candle.update(new_candle_1s)







    def test_failed_update_trade_after_candle_window(self):

        """
            Ensures candle cannot be updated with a trade after it's window
        """


        baseline_timestamp = datetime.now().replace(microsecond=0)
        price_1, price_2 = 100, 110
        first_candle_1s_a = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp,
            price_1
        )

        derived_candle = Candle_1m.start_new(candle=first_candle_1s_a)

        new_candle_1s = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            derived_candle.timestamp + timedelta(minutes=2),
            price_2
        )



        with self.assertRaises(RuntimeError):
              derived_candle.update(new_candle_1s)






    def test_failed_update_trade_on_candle_window_close(self):

        """
            Ensures candle cannot be updated with a trade on it's window close
        """

        baseline_timestamp = datetime.now().replace(microsecond=0)
        price_1, price_2 = 100, 110
        first_candle_1s_a = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp,
            price_1
        )

        derived_candle = Candle_1m.start_new(candle=first_candle_1s_a)


        new_candle_1s = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            derived_candle.timestamp + timedelta(minutes=1),
            price_2
        )


        with self.assertRaises(RuntimeError):
              derived_candle.update(new_candle_1s)





  


    def test_update(self):
        """
            Tests candle updates with a new candle correctly
        """

        baseline_timestamp = datetime.now().replace(microsecond=0)
        price_1, price_2 = 100, 110
        first_candle_1s_a = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp,
            price_1
        )


        new_candle_1s = create_single_1s_candle_with_1_trade_and_volume(
            self.symbol, 
            baseline_timestamp+timedelta(microseconds=20),
            price_2
        )

        derived_candle = Candle_1m.start_new(candle=first_candle_1s_a)
        derived_candle.update(new_candle_1s)

        pred_symbol = self.symbol
        pred_open = price_1
        pred_high = price_2
        pred_low = price_1
        pred_close = price_2

        pred_vwap_numerator = price_1 + price_2
        pred_volume = 2
        pred_trade_cnt = 2;
        pred_vwap = pred_vwap_numerator / pred_volume
        pred_timestamp = baseline_timestamp.replace(second=0)

        self.assert_candle_equal(
            candle=derived_candle,
            symbol=pred_symbol,
            open=pred_open,
            high=pred_high, 
            low=pred_low,
            close=pred_close,
            trade_cnt=pred_trade_cnt,
            volume=pred_volume,
            vwap=pred_vwap,
            timestamp=pred_timestamp,
            is_finalised=False,
            almost_equal_vwap=False
        )

        

        



    # # required for testing vwap (numerator -> vwap), volume, trade_cnt accumulation
    # def test_multiple_updates(self):
    #     """
    #         Tests candle accumulates and updates with multiple new trades correctly
    #     """

    #     aligned_timestamp = datetime.now().replace(microsecond=0)
    #     trade_cnt = 10
    #     prices = [random()*100 for _ in range(trade_cnt)]
    #     sizes = [randint(1, 150) for _ in range(trade_cnt)]
    #     trades = [
    #                 Trade(self.symbol, price=prices[i], size=sizes[i], timestamp=aligned_timestamp+timedelta(microseconds=i)) 
    #                 for i in range(trade_cnt)
    #             ]
    #     candle = Candle_1s.start_new(trades[0])
        
    #     for i in range(1, trade_cnt):
    #         candle.update(trades[i])



    #     pred_open = trades[0].price
    #     pred_high = max(prices)
    #     pred_low = min(prices)
    #     pred_close = trades[-1].price

    #     pred_vwap_numerator = sum(prices[i] * sizes[i] for i in range(trade_cnt))
    #     pred_vwap_denominator = sum(sizes)
    #     pred_volume = pred_vwap_denominator

    #     pred_timestamp = trades[0].timestamp.replace(microsecond=0)


    #     self.assert_candle_equal(
    #         candle=candle,
    #         open=pred_open,
    #         high=pred_high, 
    #         low=pred_low,
    #         close=pred_close,
    #         trade_cnt=trade_cnt,
    #         volume=pred_volume,
    #         vwap=pred_vwap_numerator/pred_vwap_denominator,
    #         timestamp=pred_timestamp,
    #         is_finalised=False,
    #         almost_equal_vwap=True
    #     )

        

