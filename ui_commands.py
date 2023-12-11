from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="start"),
        BotCommand(command="make_application", description="создание запроса")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
