from aiogram import F, Router, types
from aiogram.enums import ChatAction

from bot.utils.filters import LoggedIn, PirExpo

router = Router()


# Хендлер по отправке pdf плана выставки
@router.message(LoggedIn(), ~PirExpo(), F.text.lower().contains("план мероприятия"))
async def map_print(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.UPLOAD_DOCUMENT)

    text = "In progress..."
    await message.answer(text=text)
