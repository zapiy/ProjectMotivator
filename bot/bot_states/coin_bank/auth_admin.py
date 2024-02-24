from textwrap import dedent
from asgiref.sync import sync_to_async

from aiogram.types import Message
from typing import TYPE_CHECKING

from dashboard.models import *
from aiogram_qumit import  BotContext

if TYPE_CHECKING:
    from ._state import CoinBankState


class AuthAdminOperation:

    async def handle_auth_token(self: 'CoinBankState', message: Message, context: BotContext):
        login = message.from_user.username
        
        if context.data.get('wait_token', False):
            if await self.is_command(message, 'cancel'):
                try: await message.delete()
                except: pass
                
                context.data['wait_token'] = False
                await message.answer(dedent(f"""\
                    @{login}
                    Авторизация админ панели отменена...
                """), parse_mode="html")
            else:
                token = message.text.rstrip(' ').strip(' ')
                if (
                    ' ' in token 
                    or len(token) not in range(25, 50)
                ):
                    await message.answer(dedent(f"""\
                        @{login}
                        Ошибка: Не корректный токен
                        Отмена: /cancel
                    """), parse_mode="html")
                    return False
                else:
                    try:
                        web_admin = UserModel.objects.get(user_identity_token=token)
                        chat = await self.ensure_chat_model(message)
                        
                        chat.admin = web_admin
                        await sync_to_async(chat.save)(force_update=True)
                        
                        context.data['wait_token'] = False
                        await message.answer(dedent(f"""\
                            @{login}
                            Админ панель авторизована для токена:
                            <code>{token}</code>
                        """), parse_mode="html")
                    except UserModel.DoesNotExist:
                        await message.answer(dedent(f"""\
                            @{login}
                            Ошибка: Токен не существует
                            Отмена: /cancel
                        """))
                
            return False
            
        elif await self.is_command(message, 'webadmin'):
            if (await message.chat.get_member(message.from_user.id)).is_chat_admin():
                if await self.ensure_admin(message):
                    return False
                
                context.data['wait_token'] = True
                try: await message.delete()
                except: pass
                
                await message.answer(dedent(f"""\
                    @{login}
                    Вы перешли в процесс авторизации админ панели...
                    Что-бы завершить авторизацию введите токен
                    Или введите команду /cancel
                """))
            else:
                await message.answer(dedent(f"""\
                    @{login}
                    <b>Ошибка: Вы не администратор группы, чтобы иметь доступ к веб панели</b>
                """), parse_mode='html')

        return True
