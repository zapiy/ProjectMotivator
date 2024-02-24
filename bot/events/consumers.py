from .connection import channel
from asgiref.sync import async_to_sync
from aiogram_qumit import TelegramBot
import json

TELEGRAM_QUEUE = 'telegram'

async def handle_telegram(channel, method, properties, body):
    data = json.loads(body)
    if data["type"] == "send_message":
        user_id, text = (data["user_id"], data["text"])
        await TelegramBot().send_message(
            user_id, text,
            parse_mode='html',
        )


channel.basic_consume(
    queue=TELEGRAM_QUEUE,
    on_message_callback=async_to_sync(handle_telegram),
    auto_ack=True 
)
