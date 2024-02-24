from ..connection import channel
import json

TELEGRAM_QUEUE = 'telegram'
channel.queue_declare(queue=TELEGRAM_QUEUE) 


def send_message(user_id: int, text: str):
    channel.basic_publish(
        exchange='',
        routing_key=TELEGRAM_QUEUE,
        body=json.dumps({
            "type": "send_message",
            "user_id": user_id,
            "text": text,
        })
    )
