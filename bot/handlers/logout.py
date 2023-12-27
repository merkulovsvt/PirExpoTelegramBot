from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.funcs import User

router = Router()


# Хэндлер по выходу из системы ?
@router.message(User.logged_in, Command("logout"))
async def logout(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Вы успешно вышли из системы", reply_markup=ReplyKeyboardRemove())
    await message.answer("/start")
