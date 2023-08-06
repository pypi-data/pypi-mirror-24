from sqlalchemy import and_

from zaifbot.db.seed import CandleSticks
from .base import DaoBase


class CandleSticksDao(DaoBase):
    def __init__(self, currency_pair, period):
        super().__init__()
        self._currency_pair = str(currency_pair)
        self._period = str(period)

    def _get_model(self):
        return CandleSticks

    def get_by_time_width(self, start_time, end_time, *, closed=False):
        with self._session() as s:
            result = s.query(self._Model).filter(
                and_(self._Model.time <= end_time,
                     self._Model.time >= start_time,
                     self._Model.currency_pair == self._currency_pair,
                     self._Model.period == self._period,
                     self._Model.closed == int(closed)
                     )
            ).order_by(self._Model.time).all()
        return result
