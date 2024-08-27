from .base import *


DEBUG = True

ALLOWED_HOSTS = []

STATICFILES_DIRS = [BASE_DIR / "static"]

# MIDDLEWARE += [
#     "querycount.middleware.QueryCountMiddleware"
# ]


# QUERYCOUNT = {
#     'THRESHOLDS': {
#         'MEDIUM': 4,
#         'HIGH': 200,
#         'MIN_TIME_TO_LOG':0,
#         'MIN_QUERY_COUNT_TO_LOG':10
#     },
#     'IGNORE_REQUEST_PATTERNS': [],
#     'IGNORE_SQL_PATTERNS': [],
#     'DISPLAY_DUPLICATES': 1,
#     'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
# }


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