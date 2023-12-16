from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="make_application", description="Создание запроса"),
        BotCommand(command="add_actual_balance", description="Ввести фактический остаток"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
