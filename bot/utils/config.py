import os

from aiogram import Bot
from dotenv import load_dotenv

# Environment variables
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot_name = os.getenv("BOT_NAME")
bot_start_text = os.getenv("BOT_START_TEXT").replace(r'\n', '\n')
bot_description = os.getenv("BOT_DESCRIPTION").replace(r'\n', '\n')
bot_short_description = os.getenv("BOT_SHORT_DESCRIPTION").replace(r'\n', '\n')

server_url = os.getenv("SERVER_URL")
exhibition_name = os.getenv("EXHIBITION_NAME")
exhibition_url = os.getenv("EXHIBITION_URL")
event_program_url = os.getenv("EVENT_PROGRAM_URL")


async def set_bot_info(bot: Bot):
    current_name = (await bot.get_my_name()).name
    current_description = (await bot.get_my_description()).description
    current_short_description = (await bot.get_my_short_description()).short_description

    if current_name != bot_name:
        await bot.set_my_name(name=bot_name)

    if current_description != bot_description:
        await bot.set_my_description(description=bot_description)

    if current_short_description != bot_short_description:
        await bot.set_my_short_description(short_description=bot_short_description)
