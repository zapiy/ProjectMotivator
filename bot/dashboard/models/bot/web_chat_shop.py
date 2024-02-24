from typing import TYPE_CHECKING
from django.db import models

from ..admin import UserModel
if TYPE_CHECKING:
    from .web_chat_shop_history import BotWebChatShopHistory


class BotWebChatProducts(models.Model):
    class Meta:
        db_table = "web_shop_products"
    
    class Type(models.TextChoices):
        REAL = 'REAL'
        VIRTUAL = 'VIRTUAL'
    
    owner = models.ForeignKey(UserModel, models.CASCADE, null=True)
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.REAL,
    )
    
    image = models.ImageField(upload_to='images/motivator/')
    
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    promo_codes = models.TextField(null=True)
    is_infinity = models.BooleanField(default=False)

    sales_history: models.QuerySet['BotWebChatShopHistory']
    