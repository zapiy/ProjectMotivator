import asyncio
from textwrap import dedent
from asgiref.sync import sync_to_async

from aiogram.types import Message
from typing import TYPE_CHECKING

from dashboard.models import *
if TYPE_CHECKING:
    from ._state import CoinBankState
    

class TransferOperation:

    async def handle_transfer_operation(self: 'CoinBankState', message: Message, model: BotUserBalanceModel):
        text = message.text
        if '🪙' not in text:
            return None
        
        try:
            mention = self.MENTION_REGEX.findall(text)[0][1:].strip()
        except IndexError:
            return None
        
        if await self.ensure_admin(message):
            return False
        
        comment = self.WHITESPACE_REGEX.sub(
            ' ', 
            self.MENTION_REGEX.sub('', text)
        )
        
        try: await message.delete()
        except: pass
        
        error = None
        if mention == message.from_user.username:
            error = "Ошибка: Вы не можете перевести самому себе"
        elif model.current_balance <= 0:
            error = "Ошибка: Денег нет, но вы держитесь"

        # Working ...
        if not error:
            try:
                target = BotUserBalanceModel.objects.get(
                    binded=model.binded,
                    user=BotUserModel.objects.get(
                        platform=BotUserModel.Platform.TELEGRAM,
                        login=mention,
                    )
                )
                
                target.safe_balance += 1
                model.current_balance -= 1
                
                await sync_to_async(model.save)(force_update=True)
                await sync_to_async(target.save)(force_update=True)

                self.logger.info(f"AT {message.chat.full_name}[{message.chat.id}]; \nTRANSFER: {model.user.login} -> {target.user.login}; \nCOMMENT: \n{comment}")
                
                BotTransferHistoryModel.objects.create(
                    u_from=model,
                    u_to=target,
                )
                
                return await message.answer(dedent(f"""\
                    TRANSFER: @{model.user.login}(-1🪙) -> @{target.user.login}(+1🪙)
                    COMMENT: {comment}
                """))
                
            except (
                BotUserModel.DoesNotExist,
                BotUserBalanceModel.DoesNotExist,
            ):
                error = dedent(f"""\
                    Ошибка!!! Такого логина нет в боте.
                    Либо пользователь недавно его менял и он не обновился.
                    Либо пользователь не добавлен в бота.
                    Пусть сделает любое действие.
                """)

        if error:
            try:
                error = await message.answer(f'@{message.from_user.username}\n' + error)
                await asyncio.sleep(5)
                await error.delete()
            except:
                pass
