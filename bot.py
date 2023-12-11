import asyncio
import pygsheets

from aiogram import Bot, Dispatcher, F

from config_reader import config
from handlers import Q, main_defs
from aiogram.fsm.storage.memory import MemoryStorage
from ui_commands import set_bot_commands
from read_numers_of_members import get_all_list

bot = Bot(token=config.bot_token.get_secret_value())


# users_data.init()



# Запуск бота
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.filter(F.chat.type == "private")

    dp.include_router(Q.router)
    dp.include_router(main_defs.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
