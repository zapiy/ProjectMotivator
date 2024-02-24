from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '---'
DEBUG = True

INSTALLED_APPS = [
    'dashboard.apps.Config'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database.db',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
