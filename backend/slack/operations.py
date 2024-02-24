from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone, timedelta

from dashboard.models import *
from .middleware import WEB_CLIENT as web_client


BALANCE_LIFETIME = relativedelta(months=1)
USERDATA_CHECKTIME = timedelta(minutes=10)
DEFAULT_RESPONSE = HttpResponse()


def ensure_user_model(user_id: str) -> BotUserModel:
    model, is_created = BotUserModel.objects.get_or_create(
        platform = BotUserModel.Platform.SLACK,
        internal_id = user_id,
    )
    
    if (
        is_created 
        or (datetime.now(timezone.utc) - model.updated_at >= USERDATA_CHECKTIME)
    ):
        user_info_r = web_client.users_info(user=user_id)
        if user_info_r.status_code == 200 and user_info_r.data.get("ok", False):
            info = user_info_r.data.get("user", {})
            model.login = info['name']
            model.full_name = (
                info.get("profile", {}).get('display_name', None)
                or 
                info["real_name"]
            )
            model.save(force_update=True)
    
    return model


def ensure_chat_model(chat_id: str) -> BotChatModel:
    model, is_created = BotChatModel.objects.get_or_create(
        platform = BotChatModel.Platform.SLACK,
        internal_id = chat_id,
    )
    
    if (
        is_created 
        or (datetime.now(timezone.utc) - model.updated_at >= USERDATA_CHECKTIME)
        and web_client
    ):
        team_info_r = web_client.team_info(team=chat_id)
        if team_info_r.status_code == 200 and team_info_r.data.get("ok", False):
            info = team_info_r.data.get("team", {})
            model.full_name = info['name']
            model.save(force_update=True)
    
    return model
    

def ensure_fullstack_model(
    chat_id: str,
    user_id: str,
):
    user = ensure_user_model(user_id)
    chat = ensure_chat_model(chat_id)
    
    if not chat.users.filter(id=user.id).exists():
        chat.users.add(user)
    
    if chat.admin is None:
        return None
    
    balance, update_balance = BotUserBalanceModel.objects.get_or_create(
        binded = chat.admin,
        user = user,
    )
    
    if (
        not update_balance 
        and balance.clear_time < datetime.now(timezone.utc)
    ):
        update_balance = True
    
    if update_balance:
        balance.clear_time = datetime.now(timezone.utc) + BALANCE_LIFETIME
        balance.current_balance = 10
        
        if balance.state == balance.State.LEAVE:
            balance.safe_balance = 0
            
        balance.save(force_update=True)
    
    if balance.state == balance.State.LEAVE:
        balance.state == balance.State.NORMAL
        balance.save(force_update=True)
    
    return balance


async def destroy_chat_model(
    chat_id: int
):
    try:
        chat = BotChatModel.objects.get(
            platform=BotChatModel.Platform.SLACK,
            internal_id=chat_id
        )
    except BotChatModel.DoesNotExist:
        return
    
    chat.delete()


async def destroy_chat2user_constraints(
    user_id: str,
    chat_id: str,
):
    try:
        chat = BotChatModel.objects.get(
            platform=BotChatModel.Platform.SLACK,
            internal_id=chat_id
        )
    except BotChatModel.DoesNotExist:
        return
    
    user = ensure_user_model(user_id)
    
    if not chat.users.filter(id=user.id).exists():
        return
    
    chat.users.remove(user)
    
    if chat.admin is None:
        return 
    
    web_admin = chat.admin
    if (
        BotChatModel.objects
            .filter(
                admin=web_admin,
                users=user
            )
            .count()
    ) <= 0:
        try:
            balance = (
                BotUserBalanceModel.objects
                    .get(
                        binded=web_admin,
                        user=user
                    )
            )
            balance.state = balance.State.LEAVE
            balance.save(force_update=True)
        except BotUserBalanceModel.DoesNotExist:
            pass

