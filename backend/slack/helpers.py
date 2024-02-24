from textwrap import dedent
from dataclasses import dataclass
import logging

from .middleware import WEB_CLIENT as web_client
from slack_sdk.errors import SlackApiError

from . import modals
from . import operations


logger = logging.getLogger("SLACK")
logger.setLevel(10)

@dataclass
class UserRoutes:
    chat_id: str
    user_id: str
    trigger_id: str = None


def ensure_balance_check(
    routes: UserRoutes
):
    balance = operations.ensure_fullstack_model(routes.chat_id, routes.user_id)
    if balance is None:
        modals.text_modal(
            routes.trigger_id,
            dedent(f"""\
                У данного чата не авторизована админка
                Используйте /webadmin
            """),
        )
    return balance


def send_channel_msg( 
    channel: str,
    message: str,
    *,
    user: str = None,
    reply_ts: str = None,
    markdown: bool = True,
):
    try:
        web_client.chat_postMessage(
            channel=channel,
            thread_ts=reply_ts,
            mrkdwn=markdown,
            text=message,
        )
    except SlackApiError as err:
        if err.response.get("error", None) == "not_in_channel" and user:
            web_client.chat_postMessage(
                channel=user,
                mrkdwn=markdown,
                text=message,
            )
    return operations.DEFAULT_RESPONSE
