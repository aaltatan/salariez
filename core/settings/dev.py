import sys
from .base import *


DEBUG = True

ALLOWED_HOSTS = []

STATICFILES_DIRS = [BASE_DIR / "static"]

INSTALLED_APPS += ['silk']

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    *MIDDLEWARE,
]

# DEBUG_TOOLBAR_CONFIG = {
#     "ROOT_TAG_EXTRA_ATTRS": "hx-preserve"
# }

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

# TESTING = "test" in sys.argv

# if not TESTING:
#     INSTALLED_APPS = [
#         *INSTALLED_APPS,
#         "debug_toolbar",
#     ]
#     MIDDLEWARE = [
#         "debug_toolbar.middleware.DebugToolbarMiddleware",
#         *MIDDLEWARE,
#     ]


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'django_queries.log',  # Choose a file name and path
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }