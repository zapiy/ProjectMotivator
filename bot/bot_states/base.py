from aiogram_qumit import State, TelegramBot
from aiogram.types import *
from logging import getLogger
from dashboard.models import *

from asgiref.sync import sync_to_async
from dateutil.relativedelta import relativedelta
from datetime import datetime

BALANCE_LIFETIME = relativedelta(months=1)


class BaseState(State):
    
    def __init__(self, bot: 'TelegramBot') -> None:
        super().__init__(bot)
        
        self.logger = getLogger("bot_states")
        self.logger.setLevel(10)
    
    async def is_command(self, msg: Message, cmd: str):
        return msg.text.startswith(f"/{cmd}")
    
    @classmethod
    async def ensure_user_model(cls, message: Message) -> BotUserModel:
        if message.from_user.is_bot:
            if message.from_user.id == TelegramBot().bot_id:
                if message.chat.id > 0:
                    try:
                        return BotUserModel.objects.get(
                            platform = BotUserModel.Platform.TELEGRAM,
                            internal_id=message.chat.id,
                        )
                    except BotUserModel.DoesNotExist:
                        pass
            return None
        
        model, is_created = BotUserModel.objects.get_or_create(
            platform = BotUserModel.Platform.TELEGRAM,
            internal_id=message.from_user.id,
            defaults={
                "login": message.from_user.username,
                "full_name": message.from_user.full_name,
            }
        )
        
        if not is_created:
            re_save = False
            login, full_name = message.from_user.username, message.from_user.full_name
            
            if model.login != login:
                model.login = login
                re_save = True
                
            if model.full_name != full_name:
                model.full_name = full_name
                re_save = True
            
            if re_save:
                await sync_to_async(model.save)(force_update=True)
                
        return model


    @classmethod
    async def ensure_chat_model(cls, message: Message) -> BotChatModel:
        model, is_created = BotChatModel.objects.get_or_create(
            platform = BotChatModel.Platform.TELEGRAM,
            internal_id=message.chat.id,
            defaults={
                "full_name": message.chat.full_name,
            }
        )
        
        if not is_created:
            re_save = False
            full_name = message.chat.full_name
                
            if model.full_name != full_name:
                model.full_name = full_name
                re_save = True
            
            if re_save:
                await sync_to_async(model.save)(force_update=True)
                
        return model
    
    
    @classmethod
    async def ensure_fullstack_model(
        cls, message: Message,
    ):
        user = await cls.ensure_user_model(message)
        chat = await cls.ensure_chat_model(message)
        
        if not await sync_to_async(chat.users.filter(id=user.id).exists)():
            await sync_to_async(chat.users.add)(user)
        
        if chat.admin is None:
            return None
        
        balance, update_balance = BotUserBalanceModel.objects.get_or_create(
            binded = chat.admin,
            user = user,
        )
        
        if (
            not update_balance 
            and balance.clear_time < datetime.now()
        ):
            update_balance = True
        
        if update_balance:
            balance.clear_time = datetime.now() + BALANCE_LIFETIME
            balance.current_balance = 10
            
            if balance.state == balance.State.LEAVE:
                balance.safe_balance = 0
                
            balance.save(force_update=True)
        
        if balance.state == balance.State.LEAVE:
            balance.state == balance.State.NORMAL
            balance.save(force_update=True)
        
        return balance
    
    @classmethod
    async def destroy_chat_model(
        cls, 
        chat_id: int
    ):
        try:
            chat = BotChatModel.objects.get(
                platform=BotChatModel.Platform.TELEGRAM,
                internal_id=chat_id
            )
        except BotChatModel.DoesNotExist:
            return
        
        await sync_to_async(chat.delete)()
        """
        if chat.admin:
            if (
                BotChatModel.objects
                    .filter(admin=chat.admin)
                    .count()
            ) <= 0:
                for bal in (
                    BotUserBalanceModel.objects
                        .filter(
                            binded=chat.admin
                        )
                        .all()
                ):
                    bal.state = bal.State.LEAVE
                    await sync_to_async(bal.save)(force_update=True)
        """

    @classmethod
    async def destroy_chat2user_constraints(
        cls, 
        message: Message,
    ):
        try:
            chat = BotChatModel.objects.get(
                platform=BotChatModel.Platform.TELEGRAM,
                internal_id=message.chat.id
            )
        except BotChatModel.DoesNotExist:
            return
        
        user = await cls.ensure_user_model(message)
        
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
                await sync_to_async(balance.save)(force_update=True)
            except BotUserBalanceModel.DoesNotExist:
                pass
