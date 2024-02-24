from typing import Callable

from slack_sdk import WebClient
from django.conf import settings
from django.http import (
    HttpRequest, HttpResponseForbidden
)

BOT_UUID = settings.SLACK_BOT_UUID
VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN
ACCESS_TOKEN = settings.SLACK_ACCESS_TOKEN

WEB_CLIENT = WebClient(token=ACCESS_TOKEN)


def validate_slack(
    decode: Callable[[HttpRequest], dict] = lambda r: r.POST
):
    def wraps(func):
        def middleware(*args, **kwargs):
            request: HttpRequest = args[0]
            
            try:
                json_data = decode(request)
                if json_data.get('token', None) != VERIFICATION_TOKEN:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
            
            args = list(args)
            args.insert(1, WEB_CLIENT)
            args.insert(1, json_data)
            
            return func(*args, **kwargs)
        
        return middleware
    return wraps
