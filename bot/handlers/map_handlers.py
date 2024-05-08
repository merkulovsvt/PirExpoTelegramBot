from aiogram import F, Router, types
from aiogram.enums import ChatAction

from bot.data.tickets_data import get_pdf
from bot.utils.config import exhibition_map_url
from bot.utils.filters import LoggedIn, PirExpo

router = Router()


# Хендлер по отправке pdf плана выставки
@router.message(LoggedIn(), ~PirExpo(), F.text.lower().contains("план мероприятия"))
async def exhibition_map_print(message: types.Message):
    result = await get_pdf(url=exhibition_map_url)

    if result:
        await message.bot.send_chat_action(chat_id=message.chat.id,
                                           action=ChatAction.UPLOAD_DOCUMENT)

        await message.bot.send_document(message.chat.id, document=types.BufferedInputFile(
            file=result, filename='План мероприятия.jpg'))
    else:
        await message.reply(text="К сожалению, не можем прислать план мероприятия.")
