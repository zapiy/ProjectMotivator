from .base import *
from aiogram.enums import ChatMemberStatus


class InitialState(BaseState):
    NAME = None
    
    def __init__(self, bot: 'TelegramBot') -> None:
        super().__init__(bot)
        self.bot_login = self.bot.config['login']
        self.bot_commands = self.bot.config['commands']
        self.webapp_link = self.bot.config['webapp_link']
    
    async def on_message(self, message: Message):
        if (
            await self.is_group(message) 
            and message.from_user.is_bot
        ):
            return
        
        context = await self.get_context(message)
        
        if await self.is_group(message):
            await self.bot.inst.set_my_commands(
                self.bot_commands['chat_admin'],
                scope=BotCommandScopeChatAdministrators(message.chat.id)
            )
            await self.bot.inst.set_my_commands(
                [],
                scope=BotCommandScopeChat(message.chat.id)
            )
            
            await self.ensure_fullstack_model(message)
        
        else:
            user = await self.ensure_user_model(message)
            
            await self.bot.inst.set_chat_menu_button(
                message.chat.id,
                MenuButtonWebApp(
                    "Shop",
                    WebAppInfo(
                        url=f'{self.webapp_link}/@/web_shop/{user.user_token}/'
                    )
                )
            )
        
        self.logger.info(f"Loading cached result from {context._chat_pair}")
        await context.state.set('coin_bank')
    
    async def on_bot_chat_member_status(self, member: ChatMemberUpdated):
        self.logger.info(f"BOT STATUS AT '{member.chat.full_name}'({member.chat.id}), {member.old_chat_member.status} -> {member.new_chat_member.status}")

        if not ChatMemberStatus.is_chat_member(member.new_chat_member.status):  # Left group...
            try:
                self.destroy_chat_model(member.chat.id)
                self.logger.warning(f"BOT LEAVE FROM '{member.chat.full_name}'({member.chat.id})")
            except:
                pass
        else:
            self.logger.warning(f"BOT ADD TO '{member.chat.full_name}'({member.chat.id})")
    
    async def on_chat_member_status(self, member: ChatMemberUpdated):
        if not ChatMemberStatus.is_chat_member(member.new_chat_member.status):
            self.logger.info(f"USER LEAVE @{member.from_user.username} ({member.from_user.id}) FROM '{member.chat.full_name}'({member.chat.id})")
        else:
            self.logger.info(f"USER JOIN @{member.from_user.username} ({member.from_user.id}) TO '{member.chat.full_name}'({member.chat.id})")

    async def on_chat_member_join(self, message: Message):
        self.logger.info(f"[M] USER JOIN @{message.from_user.username} ({message.from_user.id}) TO '{message.chat.full_name}'({message.chat.id})")
        
        await self.ensure_fullstack_model(message)
        
    async def on_chat_member_leave(self, message: Message):
        self.logger.info(f"[M] USER LEAVE @{message.from_user.username} ({message.from_user.id}) FROM '{message.chat.full_name}'({message.chat.id})")
        await self.destroy_chat2user_constraints(message)
