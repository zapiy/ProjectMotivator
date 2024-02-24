from textwrap import dedent
import json, re

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.db.models import Q
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse, JsonResponse,
)

from auth.models import UserModel
from dashboard.models import *
from .middleware import validate_slack
from . import helpers
from . import operations
from . import modals

RELATIVE_MONTH = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря',]

WHITESPACE_REGEX = re.compile(' +', re.MULTILINE)
MENTION_REGEX = re.compile(r'<\B@\w+>', re.MULTILINE)

COIN_EMOJI = ':coin:'


@validate_slack(
    lambda req: json.loads(req.body.decode('utf-8'))
)
def slack_events(
    request: HttpRequest,
    json_data: dict,
    client: WebClient,
):
    if 'type' in json_data:
        if json_data['type'] == 'url_verification':
            return JsonResponse({ "challenge": json_data['challenge'] }, safe=False)
        
    if 'event' in json_data:
        event_obj = json_data.get('event', {})
        print("EVENT:", event_obj)
        
        if ('subtype' in event_obj) and (event_obj['subtype'] == 'bot_message'):
            return HttpResponse()

        elif event_obj.get('type') == 'message':
            if "bot_id" in event_obj:
                return operations.DEFAULT_RESPONSE

            routes = helpers.UserRoutes(
                event_obj['team'],
                event_obj['user'],
                # event_obj['trigger_id'],
            )
            channel = event_obj['channel']
            text = event_obj['text']
            
            balance = helpers.ensure_balance_check(routes)
            if balance is None:
                return operations.DEFAULT_RESPONSE
            
            if COIN_EMOJI in text:
                try:
                    mention = MENTION_REGEX.findall(text)[0][2:-1].strip()
                except IndexError:
                    return operations.DEFAULT_RESPONSE
                
                reply_ts=event_obj["ts"]
                
                if (mention == balance.user.internal_id):
                    return helpers.send_channel_msg(
                        channel,
                        "*Ошибка:* Вы не можете перевести коины самому себе",
                        reply_ts=reply_ts,
                        user=routes.user_id,
                    )
                elif balance.current_balance <= 0:
                    return helpers.send_channel_msg(
                        channel,
                        "*Ошибка:* Денег нет, но вы держитесь",
                        reply_ts=reply_ts,
                        user=routes.user_id,
                    )
                
                comment = WHITESPACE_REGEX.sub(' ', MENTION_REGEX.sub('', text))
                
                try:
                    target = BotUserBalanceModel.objects.get(
                        binded=balance.binded,
                        user=BotUserModel.objects.get(
                            platform=BotUserModel.Platform.SLACK,
                            internal_id=mention,
                        )
                    )
                    
                    target.safe_balance += 1
                    balance.current_balance -= 1
                    
                    balance.save(force_update=True)
                    target.save(force_update=True)

                    helpers.logger.info(dedent("""\
                        AT {target.user.login}[{target.user.internal_id}]; 
                        TRANSFER: {balance.user.login} -> {target.user.login};
                        COMMENT: \n{comment}
                    """))
                    
                    BotTransferHistoryModel.objects.create(
                        u_from=balance,
                        u_to=target,
                    )
                    
                    for chnl in [
                        channel,
                        balance.user.internal_id,
                        target.user.internal_id,
                    ]:
                        try:
                            client.chat_postMessage(
                                channel=chnl, 
                                text=dedent(f"""\
                                    TRANSFER: <@{balance.user.internal_id}>(-1🪙) -> <@{target.user.internal_id}>(+1🪙)
                                    COMMENT: {comment}
                                """)
                            )
                        except SlackApiError:
                            pass
                
                except (
                    BotUserModel.DoesNotExist,
                    BotUserBalanceModel.DoesNotExist,
                ):
                    return helpers.send_channel_msg(
                        channel,
                        reply_ts=reply_ts,
                        user=routes.user_id,
                        message=dedent(f"""\
                            Ошибка!!! Такого логина нет в боте.
                            Либо пользователь недавно его менял и он не обновился.
                            Либо пользователь не добавлен в бота.
                            Пусть сделает любое действие.
                        """)
                    )
                    
        # elif event_obj.get('type') == 'message':
        #     pass

    return HttpResponse()


@validate_slack(
    lambda req: json.loads(req.POST.get("payload", None))
)
def slack_interactive(
    request: HttpRequest,
    json_data: dict,
    client: WebClient,
):
    routes = helpers.UserRoutes(
        json_data["team"]["id"],
        json_data["user"]["id"],
        json_data["trigger_id"],
    )
    
    if "view" in json_data:
        view: dict = json_data["view"]
        if view['type'] == "modal":
            if view["callback_id"] == "auth_admin-modal":
                try:
                    token = (
                        list(
                            list(
                                view.get("state", {})
                                    .get("values", {})
                                    .values()
                            )[0].values()
                        )[0].get("value")
                    )
                except:
                    return HttpResponse()
                    
                if (
                    ' ' in token 
                    or len(token) not in range(25, 50)
                ):
                    modals.text_modal(
                        routes.trigger_id,
                        "Не корректный токен",
                    )
                else:
                    try:
                        web_admin = UserModel.objects.get(user_identity_token=token)
                        chat = operations.ensure_chat_model(routes.chat_id)
                        
                        chat.admin = web_admin
                        chat.save(force_update=True)
                        
                        modals.text_modal(
                            routes.trigger_id,
                            dedent(f"""\
                                Админ панель авторизована для админа:
                                [@{web_admin.tg_login}] (https://t.me/{web_admin.tg_login})
                            """),
                        )
                    except UserModel.DoesNotExist:
                        modals.text_modal(
                            routes.trigger_id,
                            "Не корректный токен",
                        )
    
    return HttpResponse()


@validate_slack()
def slack_balance(
    request: HttpRequest,
    json_data: dict,
    client: WebClient,
):
    routes = helpers.UserRoutes(
        json_data["team_id"],
        json_data["user_id"],
        json_data["trigger_id"],
    )
    
    balance = helpers.ensure_balance_check(routes)
    if balance is None:
        return HttpResponse()
    
    dt = balance.clear_time
    
    modals.text_modal(
        routes.trigger_id,
        title=f"Баланс {COIN_EMOJI}",
        text=dedent(f"""\
            Баланс вашего кошелька: *{balance.current_balance} монет{COIN_EMOJI}*. Вы можете их раздать в благодарность коллегам.
            Баланс обновится {dt.day} {RELATIVE_MONTH[dt.month-1]}, у вас снова станет 10 монет.
            Баланс вашего сейфа: *{balance.safe_balance} монет{COIN_EMOJI}*. Мы можете потратить их в магазине.
        """)
    )
    
    return HttpResponse()


@validate_slack()
def slack_admin_auth(
    request: HttpRequest,
    json_data: dict,
    client: WebClient,
):
    routes = helpers.UserRoutes(
        json_data["team_id"],
        json_data["user_id"],
        json_data["trigger_id"],
    )
    
    chat = operations.ensure_chat_model(routes.chat_id)
    if chat.admin is not None:
        modals.text_modal(
            routes.trigger_id,
            "Данная команда уже авторизована в админке!"
        )
        return HttpResponse()
    
    client.views_open(
        trigger_id=routes.trigger_id,
        view={
            "type": "modal",
            "callback_id": "auth_admin-modal",
            "title": {
                "type": "plain_text",
                "text": "Авторизация веб админки"
            },
            "submit": {
                "type": "plain_text",
                "text": "Okay"
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "WebAdmin token",
                        "emoji": False
                    }
                }
            ]
        }
    )
    
    return HttpResponse()

@validate_slack()
def slack_web_shop(
    request: HttpRequest,
    json_data: dict,
    client: WebClient,
):
    routes = helpers.UserRoutes(
        json_data["team_id"],
        json_data["user_id"],
        json_data["trigger_id"],
    )
    
    balance = helpers.ensure_balance_check(routes)
    if balance is None:
        return HttpResponse()
    
    modals.text_modal(
        routes.trigger_id,
        title="Магазин",
        text=f"{settings.INTERNET_URL}/@/web_shop/{balance.user.user_token}/"
    )
    
    return HttpResponse()
