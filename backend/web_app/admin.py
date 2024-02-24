from django.contrib import admin

from .models import SaleItem, DigitalItem, PhysicalItem

admin.site.register(SaleItem)
admin.site.register(DigitalItem)
admin.site.register(PhysicalItem)