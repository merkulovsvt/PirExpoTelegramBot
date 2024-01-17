import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis
from dotenv import load_dotenv

from bot.utils.config import token
from handlers import events, exhibitors, login, logout, orders
from new_handlers import tickets

load_dotenv()


async def main():
    bot = Bot(token=token)
    logging.basicConfig(level=logging.INFO)
    # await set_commands(bot)

    redis = Redis()
    dp = Dispatcher(storage=RedisStorage(redis))
    dp.include_routers(login.router, logout.router, orders.router, tickets.router, exhibitors.router, events.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
