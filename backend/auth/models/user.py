from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

from django.db import models
if TYPE_CHECKING:
    from .session import SessionModel
    from dashboard.models import BotChatModel, BotUserBalanceModel


class UserModel(models.Model):
    class Meta:
        db_table = 'sys_users'
    
    class Status(models.TextChoices):
        BLOCKED = 'BLOCK'
        DELETED = 'DELETE'
        
        GR_ADMIN = 'GR_ADM'
        
        OWNER = 'SUP_ADM'

    tg_id = models.IntegerField(db_index=True, unique=True, null=True)
    tg_login = models.CharField(max_length=100, null=True)
    
    full_name = models.CharField(max_length=170, null=True)
    
    # email: str = models.EmailField(db_index=True, unique=True, null=False)
    # password_hash: str = models.CharField(max_length=256, null=False)

    status: Status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.GR_ADMIN,
    )

    user_identity_token: str = models.UUIDField(db_index=True, unique=True, null=False, default=uuid4)
    
    updated_at: datetime = models.DateTimeField(auto_now=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    sessions: models.QuerySet['SessionModel']
    bot_chats: models.QuerySet['BotChatModel']
    bot_bills: models.QuerySet['BotUserBalanceModel']
    
    # USERNAME_FIELD = 'login'
    # REQUIRED_FIELDS = ['login']

    # def __str__(self):
    #     return self.login

    # def get_full_name(self):
    #     return str(self)

    # def get_short_name(self):
    #     return str(self)
