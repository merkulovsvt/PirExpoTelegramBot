import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from handlers import login, logout, orders


async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(logout.router, login.router, orders.router)
    # await bot.delete_webhook(drop_pending_updates=True)
    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
