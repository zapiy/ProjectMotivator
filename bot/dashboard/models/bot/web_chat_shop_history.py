from datetime import datetime
from django.db import models

from .user import BotUserModel
from .web_chat_shop import BotWebChatProducts


class BotWebChatShopHistory(models.Model):
    class Meta:
        db_table = "web_shop_history"
    
    user: BotUserModel = models.ForeignKey(
        BotUserModel, models.CASCADE, null=False,
        related_name="shop_history"
    )
    product: BotWebChatProducts = models.ForeignKey(
        BotWebChatProducts, models.CASCADE, null=False,
        related_name="sales_history"
    )
    
    is_issued: bool = models.BooleanField(null=False, default=False)
    buy_time: datetime = models.DateTimeField(auto_now=True)
