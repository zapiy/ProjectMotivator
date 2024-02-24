import asyncio
import logging

import bot.manage as manage
from decouple import config
from aiogram_qumit import *
from aiogram.types import BotCommand

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(name)s - [%(filename)s(%(lineno)d) in %(funcName)s] => %(message)s"
)
logger = logging.getLogger("main")
logger.setLevel(10)

logger.info("Create bot instance")
bot = TelegramBot(
    config("TELEGRAM_BOT_TOKEN", cast=str),
    # storage=CustomMemoryStorage(CustomMemoryStorage.ContextType.USER_ID)
)

async def main():
    logger.warning("Register states...")
    bot.config.update({
        "login": (await bot.inst.me).username,
        "webapp_link": config("INTERNET_URL", default='http://127.0.0.1:8000', cast=str),
        "commands": {
            "chat_admin": [
                BotCommand("webadmin", "Авторизовать веб админку"),
            ]
        }
    })
    bot.register_state("bot_states")
    from events import start_consuming
    start_consuming()
    await bot.run()


asyncio.run(main())

