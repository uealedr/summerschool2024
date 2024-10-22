import random
import string
import time

from otree.api import *


doc = """
Implementation of encryption task.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    TABLES = [
        "ZYXJIUTLKQSRNWVHGFEDMOPCBA",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "BADCFEHGJILKNMPORQTSVUXWZY",
    ]


class Subsession(BaseSubsession):
    payoff_per_correct = models.CurrencyField()
    time_allowed = models.IntegerField()
    random_seed = models.IntegerField()

    def setup_round(self):
        if self.round_number == 1:
            self.random_seed = self.session.config['encryption_seed']
            random.seed(self.random_seed)
        self.payoff_per_correct = Currency(self.session.config['payoff_per_correct'])
        self.time_allowed = self.session.config.get('time_allowed', 20000)
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        self.table = random.choice(C.TABLES)
        self.word = "".join(random.choices(string.ascii_uppercase, k=5))

    @property
    def reference_table(self):
        reference = {}
        for letter in string.ascii_uppercase:
            reference[letter] = self.table.index(letter) + 1
        return reference

    @property
    def correct_answer(self):
        reference = self.reference_table
        return [reference[letter] for letter in self.word]


class Player(BasePlayer):
    started_round = models.FloatField()
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField(initial=False)

    def get_response_fields(self):
        return ['response_1', 'response_2', 'response_3', 'response_4', 'response_5']

    @property
    def response(self):
        return [self.response_1, self.response_2, self.response_3, self.response_4, self.response_5]

    @property
    def time_remaining(self):
        return self.subsession.time_allowed - (time.time() - self.in_round(1).started_round)

    def start_task(self) -> None:
        self.started_round = time.time()

    def determine_outcome(self, timeout_happened):
        if timeout_happened:
            self.response_1 = None
            self.response_2 = None
            self.response_3 = None
            self.response_4 = None
            self.response_5 = None
        else:
            self.is_correct = (self.response == self.group.correct_answer)
            if self.is_correct:
                self.payoff = self.subsession.payoff_per_correct

    @property
    def total_correct(self):
        return sum(p.is_correct for p in self.in_all_rounds())

    @property
    def attempted(self):
        return self.field_maybe_none('response_1') is not None

    @property
    def total_attempted(self):
        return sum(p.attempted for p in self.in_all_rounds())

    @property
    def total_payoff(self):
        return sum(p.payoff for p in self.in_all_rounds())


def creating_session(subsession: Subsession):
    subsession.setup_round()


class StartTask(Page):
    @staticmethod
    def is_displayed(player: Player) -> bool:
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool) -> None:
        player.start_task()


class EncryptionPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return player.get_response_fields()

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 or player.time_remaining > 0

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_remaining

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.determine_outcome(timeout_happened)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.effort_score = player.total_correct


page_sequence = [
    StartTask,
    EncryptionPage,
    Results,
]
