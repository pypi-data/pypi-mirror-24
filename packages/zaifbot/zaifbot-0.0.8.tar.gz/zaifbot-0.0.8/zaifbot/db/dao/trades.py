from zaifbot.db.seed import Trades
from .base import DaoBase


class TradesDao(DaoBase):
    def _get_model(self):
        return Trades

    def history(self, from_datetime, to_datetime, filters=None):
        with self._session() as s:

            q = s.query(self._Model)

            if from_datetime is not None:
                q = q.filter(self._Model.entry_datetime >= from_datetime)

            if to_datetime is not None:
                q = q.filter(self._Model.exit_datetime <= to_datetime)

            if filters is None:
                return q.all()

            if not isinstance(filters, dict):
                raise TypeError("params should be 'dict'")

            q = self._custom_filters(q, filters)
            return q.all()
