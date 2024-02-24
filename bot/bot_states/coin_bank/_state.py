from logging import getLogger
from textwrap import dedent
import re

from aiogram_qumit.extended_states.inline import InlineSelectorState
from ..base import *
from .transfer import TransferOperation
from .auth_admin import AuthAdminOperation


class CoinBankState(BaseState, TransferOperation, AuthAdminOperation):
    NAME = "coin_bank"

    RELATIVE_MONTH = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря',]

    WHITESPACE_REGEX = re.compile(' +', re.MULTILINE)
    MENTION_REGEX = re.compile(r'\B@\w+', re.MULTILINE)
    
    USER_WAYS = {
        "Баланс 🪙": "balance",
    }
    
    def __init__(self, bot: 'TelegramBot') -> None:
        super().__init__(bot)
        self.bot_id = self.bot.inst.id
        self.bot_login = self.bot.config['login']
        self.bot_commands = self.bot.config['commands']
        
        self.USER_KEYBOARD = self.gen_reply_keyboard(self.USER_WAYS)
        
        self.logger = getLogger("coin_bank")
        self.logger.setLevel(10)

    async def on_enter(self, message: Message):
        return await self.on_message(message)
    
    async def ensure_admin(self, message: Message):
        member = await self.bot.inst.get_chat_member(message.chat.id, self.bot_id)
        if member.is_chat_admin():
            return False
        await message.reply(dedent("""\
            К превеликому сожалению операции с ботом не доступны, 
            если он не администратор <b>;)</b>
        """), parse_mode="html")
        return True
    
    async def on_message(self, message: Message):
        context = await self.get_context(message)
        
        if await self.is_group(message):
            balance = await self.ensure_fullstack_model(message)
            
            if balance is None:
                await self.handle_auth_token(message, context)
            else:
                await self.handle_transfer_operation(message, balance)
            
        else:
            user = await self.ensure_user_model(message)
            
            way = None
            if not await InlineSelectorState.was_used(context):
                try:
                    way = self.USER_WAYS[message.text]
                except KeyError:
                    return await message.answer(
                        "Выберите одну из доступных операций!",
                        reply_markup=self.USER_KEYBOARD
                    )
            
            if (
                way == "balance" 
                or await InlineSelectorState.was_used(context, "balance")
            ):                    
                admins = (
                    UserModel.objects
                        .filter(bot_bills__user=user)
                        .values("id", "tg_login")
                )
                
                if admins.count() >= 1:
                    selected = await InlineSelectorState.output(context)
                    
                    if selected is not None and selected.startswith("bal-"):
                        try:
                            balance = (
                                BotUserBalanceModel.objects
                                    .filter(
                                        user=user,
                                        binded_id=int(selected[4::]),
                                    )
                                    .get()
                            )
                            
                            dt = balance.clear_time
                            return await message.answer(dedent(f"""\
                                <b>By @{balance.binded.tg_login}</b>
                                Баланс вашего кошелька: <b>{balance.current_balance} монет🪙</b>. Вы можете их раздать в благодарность коллегам.
                                Баланс обновится {dt.day} {self.RELATIVE_MONTH[dt.month-1]}, у вас снова станет 10 монет.
                                Баланс вашего сейфа: <b>{balance.safe_balance} монет🪙</b>. Мы можете потратить их в магазине.
                            """), parse_mode="html")
                        except (
                            ValueError,
                            BotUserBalanceModel.DoesNotExist,
                        ): pass
                
                    await InlineSelectorState.push(
                        context, "balance",
                        "Выберите администратора вашей группы",
                        ways={
                            f"@{bal['tg_login']}": f"bal-{bal['id']}"
                            for bal in admins.all()
                        },
                        rows_count=2
                    )
                    
                else:
                    return await message.answer(
                        "<b>Ошибка:</b> Вы не состоите ни в одной группе c ботом!",
                        parse_mode="html"
                    )
