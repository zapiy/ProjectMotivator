from typing import TYPE_CHECKING
from uuid import uuid4

from django.db import models
if TYPE_CHECKING:
    from .chat import BotChatModel
    from .balance import BotUserBalanceModel
    

class BotUserModel(models.Model):
    class Meta:
        db_table = 'bot_users'
    
    class Platform(models.TextChoices):
        TELEGRAM = 'TG'
        SLACK = 'SLC'
    
    platform: Platform = models.CharField(
        max_length=15,
        choices=Platform.choices,
        default=Platform.TELEGRAM,
        db_index=True,
    )
    internal_id: str = models.CharField(null=False, db_index=True, max_length=100)
    
    login: str = models.CharField(null=True, max_length=100)
    full_name: str = models.CharField(null=True, max_length=150)
    
    user_token: str = models.UUIDField(db_index=True, unique=True, null=False, default=uuid4)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    chats: models.QuerySet['BotChatModel']
    balances: models.QuerySet['BotUserBalanceModel']
