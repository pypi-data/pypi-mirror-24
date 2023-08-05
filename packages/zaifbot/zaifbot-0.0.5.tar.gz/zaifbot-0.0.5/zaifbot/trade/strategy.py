import time
from zaifbot.exchange.api.http import BotTradeApi
from zaifbot.logger import bot_logger


class Strategy:
    # todo: able to handle multiple rules
    def __init__(self, entry_rule, exit_rule, stop_rule=None):
        self._trade_api = BotTradeApi()
        self._entry_rule = entry_rule
        self._exit_rule = exit_rule
        self._stop_rule = stop_rule
        self._trade = None
        self._have_position = False
        self._alive = False

    def _need_stop(self):
        if self._stop_rule:
            return self._stop_rule.need_stop()

    def _entry(self):
        self._trade = self._entry_rule.entry()
        self._have_position = True

    def _exit(self):
        self._exit_rule.exit(self._trade)
        self._have_position = False

    def _check_entry(self):
        if self._entry_rule.can_entry():
            self._entry()

    def _check_exit(self):
        if self._exit_rule.can_exit(self._trade):
            self._exit()

    def start(self, *, sec_wait=1):
        # fixme
        self._alive = True
        while self._alive:
            # fixme: output to console too
            bot_logger.info('alive')
            self.regular_job()
            if self._need_stop():
                break
            if self._have_position:
                bot_logger.info('check exit')
                self._check_exit()
            else:
                bot_logger.info('check entry')
                self._check_entry()
            time.sleep(sec_wait)
        else:
            pass

    def regular_job(self):
        pass

    def stop(self):
        self._alive = False
