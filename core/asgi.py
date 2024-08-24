"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from blacknoise import BlackNoise

settings_module: str = 'dev' if os.getenv('DEBUG') == '1' else 'prod'

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    f"core.settings.{settings_module}"
)

application = BlackNoise(get_asgi_application())
application.add('static', 'static')