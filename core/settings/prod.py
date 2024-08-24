from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(';')

STATIC_ROOT = BASE_DIR / 'static'