from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="make_application", description="Создание запроса"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
