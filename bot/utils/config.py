import os

from aiogram import Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv

# Environment variables
load_dotenv()

token = os.getenv("BOT_TOKEN")


async def set_commands(bot: Bot):
    await bot.set_my_commands([BotCommand(command="start", description="Регистрация"),
                               BotCommand(command="info", description="Информация")])
