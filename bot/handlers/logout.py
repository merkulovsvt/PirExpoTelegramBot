from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.states import User

router = Router()


# Хендлер по выходу из системы +
@router.message(User.logged_in, Command("logout"))
async def logout(message: Message, state: FSMContext):
    await message.answer("Вы успешно вышли из системы", reply_markup=ReplyKeyboardRemove())

    await message.answer("/start")
    await state.clear()
