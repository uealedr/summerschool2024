import random
import string

from otree.api import *


doc = """
Implementation of encryption task.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    TABLES = [
        "ZYXJIUTLKQSRNWVHGFEDMOPCBA",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "BADCFEHGJILKNMPORQTSVUXWZY",
    ]


class Subsession(BaseSubsession):
    payoff_per_correct = models.CurrencyField()
    random_seed = models.IntegerField()

    def setup_round(self):
        if self.round_number == 1:
            self.random_seed = self.session.config['encryption_seed']
            random.seed(self.random_seed)
        self.payoff_per_correct = Currency(self.session.config['payoff_per_correct'])
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        self.table = random.choice(C.TABLES)
        self.word = random.choices(string.ascii_uppercase, k=5)

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

    def determine_outcome(self):
        self.is_correct = (self.response == self.group.correct_answer)
        if self.is_correct:
            self.payoff = self.subsession.payoff_per_correct


def creating_session(subsession: Subsession):
    subsession.setup_round()


# PAGES
class EncryptionPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return player.get_response_fields()

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.determine_outcome()


class Results(Page):
    pass


page_sequence = [
    EncryptionPage,
    # Results,
]
