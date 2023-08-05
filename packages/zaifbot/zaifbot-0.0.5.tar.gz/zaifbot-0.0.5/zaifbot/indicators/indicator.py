from abc import ABCMeta, abstractmethod
from talib import abstract
from pandas import DataFrame
from zaifbot.exchange.candle_sticks import CandleSticks
from zaifbot.exchange.currency_pairs import CurrencyPair
from zaifbot.exchange.period import Period


class Indicator(metaclass=ABCMeta):
    _MAX_LENGTH = 100
    _MAX_COUNT = 1000
    _NAME = None

    def __init__(self, currency_pair, period):
        self._currency_pair = CurrencyPair(currency_pair)
        self._period = Period(period)

    @abstractmethod
    def request_data(self, *args, **kwargs):
        raise NotImplementedError

    def _exec_talib_func(self, *args, **kwargs):
        return abstract.Function(self.name)(*args, **kwargs)

    def _get_candlesticks_df(self, count, to_epoch_time):
        required_data_count = self._required_candlesticks_count(count)

        candle_sticks_data = CandleSticks(
            self._currency_pair,
            self._period
        ).request_data(required_data_count, to_epoch_time)

        return DataFrame(candle_sticks_data)

    @property
    def name(self):
        return self._NAME

    @classmethod
    def _bounded_length(cls, value):
        return min(max(value, 0), cls._MAX_LENGTH)

    @classmethod
    def _bounded_count(cls, value):
        return min(max(value, 0), cls._MAX_COUNT)

    @abstractmethod
    def _required_candlesticks_count(self, count):
        raise NotImplementedError
