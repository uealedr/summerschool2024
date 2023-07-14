from otree.api import *


doc = """
Implementation of encryption task.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class EncryptionPage(Page):
    pass


class Results(Page):
    pass


page_sequence = [
    EncryptionPage,
    # Results,
]
