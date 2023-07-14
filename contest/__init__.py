from otree.api import *


doc = """
Tullock contest app
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 20
    EXCHANGE_VALUE = Currency(1)


class Subsession(BaseSubsession):
    def setup_round(self):
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    ticket_drawn = models.IntegerField()
    is_sequential = models.BooleanField()

    def setup_round(self):
        is_sequential = False
        for player in self.get_players():
            player.setup_round()


class Player(BasePlayer):
    endowment = models.IntegerField()
    exchange_value = models.CurrencyField()
    tickets_entered = models.IntegerField()
    amount_won = models.CurrencyField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.exchange_value = C.EXCHANGE_VALUE


def creating_session(subsession: Subsession):
    subsession.setup_round()


# PAGES
class EnterTickets(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        return ['tickets_entered']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [
    EnterTickets,
    ResultsWaitPage,
    Results
]
