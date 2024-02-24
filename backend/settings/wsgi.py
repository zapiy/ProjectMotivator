"""
WSGI config for settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(name)s - [%(filename)s(%(lineno)d) in %(funcName)s] => %(message)s"
)

application = get_wsgi_application()

