import random

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
    PRIZE = Currency(20)


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

    def determine_outcome(self):
        tickets = []
        for player in self.get_players():
            for _ in range(player.tickets_entered):
                tickets.append(player)
        if len(tickets) > 0:
            self.ticket_drawn = random.randint(1, len(tickets))
            tickets[self.ticket_drawn - 1].amount_won = C.PRIZE
        else:
            self.ticket_drawn = 0
            random.choice(self.get_players()).amount_won = C.PRIZE


class Player(BasePlayer):
    endowment = models.IntegerField()
    exchange_value = models.CurrencyField()
    tickets_entered = models.IntegerField()
    amount_won = models.CurrencyField(initial=Currency(0))

    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.exchange_value = C.EXCHANGE_VALUE

    @property
    def other_player(self):
        return self.get_others_in_group()[0]

def creating_session(subsession: Subsession):
    subsession.setup_round()


# PAGES
class EnterTickets(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        return ['tickets_entered']


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.determine_outcome()


class Results(Page):
    pass


page_sequence = [
    EnterTickets,
    ResultsWaitPage,
    Results
]
