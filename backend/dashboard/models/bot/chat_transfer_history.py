from datetime import datetime
from django.db import models

from .balance import BotUserBalanceModel


class BotTransferHistoryModel(models.Model):
    class Meta:
        db_table = 'bot_transfer_history'

    u_from = models.ForeignKey(
        BotUserBalanceModel, models.CASCADE, 
        related_name='spends', null=False
    )
    
    u_to = models.ForeignKey(
        BotUserBalanceModel, models.CASCADE,
        related_name='refills', null=False
    )

    count: int = models.IntegerField(null=False, default=1)
    transfer_time: datetime = models.DateTimeField(auto_now_add=True)
    