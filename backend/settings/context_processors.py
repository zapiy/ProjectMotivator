from django.conf import settings


def settings_context(request):
    return {
        'INTERNET_URL': settings.INTERNET_URL
    }
