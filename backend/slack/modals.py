from .operations import DEFAULT_RESPONSE
from .middleware import WEB_CLIENT as web_client


def text_modal(
    trigger_id: str,
    text: str,
    title: str = "Ошибка!"
):
    web_client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            # "callback_id": "simple-modal",
            "title": {
                "type": "plain_text",
                "text": title,
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text,
                    }
                }
            ]
        }
    )
    return DEFAULT_RESPONSE
