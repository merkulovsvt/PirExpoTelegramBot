import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import events, exhibitors, orders, partners, tickets, user

from bot.handlers import timetable
from bot.utils.config import set_commands, token


async def main():
    bot = Bot(token=token)
    logging.basicConfig(level=logging.INFO)
    await set_commands(bot)

    dp = Dispatcher()
    dp.include_routers(user.router, orders.router, tickets.router, exhibitors.router, events.router, timetable.router,
                       partners.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
