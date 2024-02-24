from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.conf import settings

from ..models import SessionModel


def ensure_auth_control(redirect_to=settings.LOGIN_URL):
    def wraps(func):
        def middleware(*args, **kwargs):
            request: HttpRequest = args[0]
            session: SessionModel = request.session._model
            
            if session.user is None:
                if redirect_to:
                    return redirect(redirect_to)
                return HttpResponseForbidden()
            
            request.session._user = session.user
            return func(*args, **kwargs)

        return middleware
    return wraps
