"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise


DEBUG = os.getenv('DEBUG') == '1'
settings_module: str = 'dev' if DEBUG else 'prod'

os.environ.setdefault(
  "DJANGO_SETTINGS_MODULE", f"core.settings.{settings_module}"
)

application = WhiteNoise(get_wsgi_application(), 'static')
