from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.data import User

router = Router()


@router.message(User.logged_in, F.text.lower() == "logout")
async def logout(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Вы успешно вышли из системы", reply_markup=ReplyKeyboardRemove())
    await message.answer("/start")
