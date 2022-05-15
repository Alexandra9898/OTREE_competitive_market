from os import environ

SESSION_CONFIGS = [
    dict(
        name='control_group_NR',
        app_sequence=['control_group_NR'],
        num_demo_participants=6,  # 12
    ),
    dict(
        name='evalutaion_group_R',
        app_sequence=['evaluation_group_R'],
        num_demo_participants=6,  # 12
    ),
    dict(
        name='evalutaion_group_R1',
        app_sequence=['evaluation_group_R1'],
        num_demo_participants=6,  # 12
    ),
    dict(
        name='evalutaion_group_R2',
        app_sequence=['evaluation_group_R2'],
        num_demo_participants=6,  # 12
        ),
    dict(
        name='formal_evaluation_group_R',
        app_sequence=['experiment_survey', 'evaluation_group_R', 'Survey'],
        num_demo_participants=6
        ),  # 12
    dict(
        name='formal_evaluation_group_R1',
        app_sequence=['experiment_survey', 'evaluation_group_R1', 'Survey'],
        num_demo_participants=6
        ),  # 12,
    dict(
        name='formal_evaluation_group_R2',
        app_sequence=['experiment_survey', 'evaluation_group_R2', 'Survey'],
        num_demo_participants=6
        ),  # 12
    dict(
        name='formal_control_group_NR',
        app_sequence=['experiment_survey_NR', 'control_group_NR', 'Survey_NR'],
        num_demo_participants=6
        )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4390865359451'
PARTICIPANT_FIELDS=["role"]
