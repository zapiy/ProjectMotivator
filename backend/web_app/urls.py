from django.contrib import admin
from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', views.index, name='index'),
                  path('items_view', views.items_view, name='items_view'),
                  path('digital_item_create', views.digital_item_create, name='digital_item_create'),
                  path('physical_item_create', views.physical_item_create, name='physical_item_creation'),
                  path('buy_item/<int:item_id>', views.buy_item, name='buy_item'),
                  path('edit_item/<int:item_id>', views.edit_item, name='edit_item'),
                  path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
