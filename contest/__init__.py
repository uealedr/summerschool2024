import random

from otree.api import *


doc = """
Tullock contest app
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = [20, 30]
    EXCHANGE_VALUE = Currency(1)
    PRIZE = Currency(20)


class Subsession(BaseSubsession):
    is_paid = models.BooleanField(initial=False)

    def setup_round(self):
        if self.round_number == 1:
            self.is_paid = True
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    ticket_drawn = models.IntegerField()
    is_sequential = models.BooleanField()

    def setup_round(self):
        self.is_sequential = False
        players = sorted(self.get_players(), key=lambda p: p.effort_score)
        players[0].endowment = C.ENDOWMENT[0]
        players[1].endowment = C.ENDOWMENT[1]
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
        for player in self.get_players():
            player.determine_earnings()


class Player(BasePlayer):
    endowment = models.IntegerField()
    exchange_value = models.CurrencyField()
    tickets_entered = models.IntegerField()
    amount_won = models.CurrencyField(initial=Currency(0))
    earnings = models.CurrencyField(initial=Currency(0))

    def setup_round(self):
        self.exchange_value = C.EXCHANGE_VALUE

    @property
    def other_player(self):
        return self.get_others_in_group()[0]

    @property
    def is_second_mover(self):
        return self.group.is_sequential and self.id_in_group == 2

    def determine_earnings(self):
        self.earnings = (self.endowment - self.tickets_entered) * self.exchange_value + self.amount_won
        if self.subsession.is_paid:
            self.payoff = self.earnings

    @property
    def effort_score(self):
        try:
            return self.participant.effort_score
        except KeyError:
            if self.id_in_group == 2:
                return 2
            else:
                return 1

# PAGES
class SetupContest(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(subsession):
        for subs in subsession.in_all_rounds():
            subs.setup_round()


class EnterTickets1(Page):
    form_model = 'player'
    template_name = 'contest/EnterTickets.html'

    @staticmethod
    def is_displayed(player):
        return not player.group.is_sequential or player.id_in_group == 1

    @staticmethod
    def get_form_fields(player):
        return ['tickets_entered']


class FirstMoverWaitPage(WaitPage):
    pass


class EnterTickets2(Page):
    form_model = 'player'
    template_name = 'contest/EnterTickets.html'

    @staticmethod
    def is_displayed(player):
        return player.is_second_mover

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
    SetupContest,
    EnterTickets1,
    FirstMoverWaitPage,
    EnterTickets2,
    ResultsWaitPage,
    Results
]
