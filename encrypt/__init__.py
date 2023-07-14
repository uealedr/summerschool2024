from otree.api import *


doc = """
Implementation of encryption task.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    def setup_round(self):
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        self.table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.word = "ZZYZX"


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField(initial=False)


def creating_session(subsession: Subsession):
    subsession.setup_round()


# PAGES
class EncryptionPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return ['response_1', 'response_2', 'response_3', 'response_4', 'response_5']


class Results(Page):
    pass


page_sequence = [
    EncryptionPage,
    # Results,
]
