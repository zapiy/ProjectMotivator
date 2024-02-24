from django.urls import path
from . import views

app_name = 'slack'
urlpatterns = [
    path('events/', view=views.slack_events, name='events'),
    path('interactive/', view=views.slack_interactive, name='interactive'),
    path('cmd/balance/', view=views.slack_balance, name='cmd_balance'),
    path('cmd/auth_admin/', view=views.slack_admin_auth, name='cmd_auth'),
    path('cmd/web_shop/', view=views.slack_web_shop, name='cmd_shop'),
]
