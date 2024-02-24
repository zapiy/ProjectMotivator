from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '---'
DEBUG = True

INSTALLED_APPS = [
    'dashboard.apps.Config'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roket_team',
        'USER': 'roket_team',
        'PASSWORD': '8awf3oHn4X4fWZY1',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
