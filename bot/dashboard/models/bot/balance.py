from typing import TYPE_CHECKING
from django.db import models

from ..admin import UserModel
from .user import BotUserModel
if TYPE_CHECKING:
    from .chat_transfer_history import BotTransferHistoryModel
    from .web_chat_shop_history import BotWebChatShopHistory


class BotUserBalanceModel(models.Model):
    class Meta:
        db_table = 'bot_user_balance'

    class State(models.TextChoices):
        NORMAL = 'NORMAL'
        LEAVE = 'LEAVE'
    
    binded = models.ForeignKey(
        UserModel, models.CASCADE, 
        related_name='bot_bills', null=False
    )
    
    user = models.ForeignKey(
        BotUserModel, models.CASCADE, 
        related_name='balances', null=False
    )
    
    state: State = models.CharField(
        max_length=15,
        choices=State.choices,
        default=State.NORMAL,
    )

    current_balance = models.IntegerField(null=False, default=10)
    safe_balance = models.IntegerField(null=False, default=0)

    clear_time = models.DateTimeField(null=True)

    spends: models.QuerySet['BotTransferHistoryModel']
    refills: models.QuerySet['BotTransferHistoryModel']
    shop_history: models.QuerySet['BotWebChatShopHistory']
    