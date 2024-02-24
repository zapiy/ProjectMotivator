from typing import Callable
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.utils.crypto import get_random_string
from django.conf import settings

from ..models import SessionModel
import string 


VALID_KEY_CHARS = (
    string.ascii_lowercase + string.digits 
    + string.ascii_uppercase
)

class CsrfMiddleware:
    IGNORE_PATHS = [
        ("/media/" if settings.MEDIA_URL == '/' else settings.MEDIA_URL),
        (settings.STATIC_URL or "/static/"),
        *(settings.CSRF_IGNORE_PATHS or [])
    ]
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        
        if any([request.path.startswith(l) for l in self.IGNORE_PATHS]):  
            return self.get_response(request)
        
        if (
            request.session.session_key is None
            or not request.session.exists(request.session.session_key)
        ):
            request.session.create()
            del request.session._session_cache
            
        request.session._get_session()
        
        model: SessionModel = request.session._model
        cookies_token = request.COOKIES.get(settings.CSRF_COOKIE_NAME, None)

        if (
            model.csrf_token is not None
            and model.csrf_token != cookies_token
        ):
            resp = HttpResponseForbidden('Request forgery attempt: Incorrect csrf token!')
            resp.delete_cookie(settings.SESSION_COOKIE_NAME)
            resp.delete_cookie(settings.CSRF_COOKIE_NAME)
            return resp
        
        response = self.get_response(request)
        
        model.csrf_token = self.apply_cookie(response)
        model.save(force_update=True)

        return response
    
    def apply_cookie(self, response: HttpResponse):
        val = get_random_string(30, VALID_KEY_CHARS)
        response.set_cookie(
            settings.CSRF_COOKIE_NAME, val,
            max_age=settings.CSRF_COOKIE_AGE,
            domain=settings.CSRF_COOKIE_DOMAIN,
            path=settings.CSRF_COOKIE_PATH,
            secure=settings.CSRF_COOKIE_SECURE,
            httponly=settings.CSRF_COOKIE_HTTPONLY,
            samesite=settings.CSRF_COOKIE_SAMESITE,
        )
        return val


# from django.middleware.csrf import CsrfViewMiddleware
# from django.contrib.sessions.middleware import SessionMiddleware
