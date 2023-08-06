from zaifbot.rules.rule import Rule
from zaifbot.exchange.action import Action
from zaifbot.exchange.currency_pairs import CurrencyPair


class Entry(Rule):
    def __init__(self, currency_pair, amount, action='bid', name=None):
        self.currency_pair = CurrencyPair(currency_pair)
        self.amount = amount
        self.action = Action(action)
        self.name = name or self.__class__.__name__

    def can_entry(self, *args, **kwargs):
        raise NotImplementedError

    def entry(self, trade):
        trade.entry(currency_pair=self.currency_pair,
                    amount=self.amount,
                    action=self.action)

        return trade
