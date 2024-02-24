from django.apps import AppConfig


class AuthConfig(AppConfig):
    label = 'auth'
    name = 'auth'
    models_module = "auth.models"

# python3.7 manage.py makemigrations auth
