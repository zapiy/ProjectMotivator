from django.db import models


class SaleItem(models.Model):
    image = models.ImageField(upload_to='images/motivator/')
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

class DigitalItem(SaleItem):
    promo_codes = models.TextField()


class PhysicalItem(SaleItem):
    count = models.PositiveIntegerField()
    is_infinity = models.BooleanField()
