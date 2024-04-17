import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.handlers import (events_handlers, exhibitors_handlers,
                          orders_handlers, partners_handlers, tickets_handlers,
                          timetable_handlers, user_handlers)
from bot.utils.config import token


async def main():
    bot = Bot(token=token)
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_routers(user_handlers.router, orders_handlers.router, tickets_handlers.router,
                       exhibitors_handlers.router, events_handlers.router, timetable_handlers.router,
                       partners_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
