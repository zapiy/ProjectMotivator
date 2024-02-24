import json
from logging import getLogger
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import (
    HttpRequest, JsonResponse
)

from middleware import methods_only
from .models import UserModel, SessionModel
from . import validators

logger = getLogger("auth:views")
logger.setLevel(10)


@methods_only('POST')
def register(request: HttpRequest):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"errors": ["Incorrect JSON"]}, status=400)
    
    if not all([k in data for k in ['email', 'password']]):
        return JsonResponse({"errors": ["No required API keys [email, password]"]}, status=400)
    
    errors = []
    email, password = [i.rstrip(' ') for i in [data['email'], data['password']]]
    
    if not validators.email(email):
        errors.append("Не корректный email!")
    elif UserModel.objects.filter(email=email).exists():
        errors.append("Пользователь с такой почтой уже существует!")
    else:
        errors.extend(validators.password(password))
    
    if len(errors) > 0:
        return JsonResponse({"errors": errors}, status=400)
    
    logger.warning(f"Register new user Email: {email}")
    user: UserModel = UserModel.objects.create(
        email=email,
        password_hash=make_password(password)
    )
    user.sessions.add(request.session._model)
    
    return JsonResponse({"redirect_to": settings.LOGIN_REDIRECT_URL}, status=200)


@methods_only('POST')
def auth(request: HttpRequest):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"errors": ["Incorrect JSON"]}, status=400)
    
    if not all([k in data.keys() for k in ['email', 'password']]):
        return JsonResponse({"errors": ["No required API keys [email, password]"]}, status=400)
    
    errors = []
    email, password = [i.rstrip(' ') for i in [data['email'], data['password']]]
    
    if not validators.email(email):
        errors.append("Не корректный email!")
    elif not UserModel.objects.filter(email=email).exists():
        errors.append("Пользователь с такой почтой не существует!")
    
    user: UserModel = None
    session: SessionModel = request.session._model
    
    if len(errors) == 0:
        user: UserModel = UserModel.objects.get(email=email)
        if session.user is not None:
            return JsonResponse({"redirect_to": settings.LOGIN_REDIRECT_URL}, status=200)
        elif not check_password(password, user.password_hash):
            errors.append("Пароль не верный!")
    
    if len(errors) > 0:
        return JsonResponse({"errors": errors}, status=400)
    
    user.sessions.add(session)
    return JsonResponse({"redirect_to": settings.LOGIN_REDIRECT_URL}, status=200)
