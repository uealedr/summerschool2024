from os import environ

SESSION_CONFIGS = [
    dict(
        name='encryption_task',
        app_sequence=[
            'encrypt',
        ],
        num_demo_participants=3,
        payoff_per_correct="0.10",
        encryption_seed=12345,
    ),
    dict(
        name='contest_task',
        app_sequence=[
            'contest',
        ],
        num_demo_participants=2,
    ),
    dict(
        name='combined',
        app_sequence=[
            'encrypt',
            'contest',
        ],
        payoff_per_correct="0.10",
        encryption_seed=12345,
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['effort_score']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8919146369583'
