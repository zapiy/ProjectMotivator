from datetime import datetime
from django.db import models

from .user import BotUserModel
from ..admin import UserModel


class BotChatModel(models.Model):
    class Meta:
        db_table = 'bot_chats'

    class Platform(models.TextChoices):
        TELEGRAM = 'TG'
        SLACK = 'SLC'
    
    admin = models.ForeignKey(
        UserModel, models.CASCADE, null=True,
        related_name="bot_chats"
    )
    
    platform: Platform = models.CharField(
        max_length=15,
        choices=Platform.choices,
        default=Platform.TELEGRAM,
        db_index=True,
    )
    internal_id: str = models.CharField(null=False, db_index=True, max_length=100)
    
    full_name: str = models.CharField(null=True, max_length=170)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    users = models.ManyToManyField(BotUserModel, related_name='chats')
