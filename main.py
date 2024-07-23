import logging

from aiogram import Bot, Dispatcher, types
from aiohttp import web

from bot.handlers import (events_handlers, exhibitors_handlers,
                          orders_handlers, partners_handlers, tickets_handlers,
                          timetable_handlers, user_handlers, map_handlers)
from bot.utils.config import bot_token, host_url, set_bot_info, bot_name

bot = Bot(token=bot_token)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_routers(user_handlers.router, orders_handlers.router, tickets_handlers.router,
                   exhibitors_handlers.router, events_handlers.router, timetable_handlers.router,
                   partners_handlers.router, map_handlers.router)


async def set_webhook():
    webhook_url = host_url + f'/{bot_token}'
    await bot.set_webhook(webhook_url, drop_pending_updates=True)


async def on_startup(_):
    await set_webhook()
    await set_bot_info(bot=bot)
    await bot.send_message(chat_id=490082094, text=f'Bot {bot_name} has been started')


async def on_shutdown(_):
    await bot.send_message(chat_id=490082094, text=f'Bot {bot_name} has been started')


app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]

    if token == bot_token:
        update = types.Update(**await request.json())
        await dp.feed_update(bot=bot, update=update)
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post(f'/{bot_token}', handle_webhook)

if __name__ == "__main__":
    web.run_app(app=app, host='localhost', port=9000)
