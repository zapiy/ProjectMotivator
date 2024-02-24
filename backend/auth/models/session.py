from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.sessions.models import SessionManager
from django.contrib.sessions.base_session import AbstractBaseSession
from ..db.session_engine import SessionStore

from .user import UserModel


class SessionModel(AbstractBaseSession):
    session_key = models.CharField(_('session key'), max_length=100, primary_key=True)
    csrf_token: str = models.CharField(_('csrf token'), max_length=60, null=True)
    expire_date = models.DateTimeField(_('expire date'), db_index=True, null=True)
    
    user: UserModel = models.ForeignKey(
        UserModel, related_name="sessions", 
        on_delete=models.SET_NULL, null=True,
    )
    
    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    class Meta(AbstractBaseSession.Meta):
        db_table = 'sys_session'
        abstract = False
    