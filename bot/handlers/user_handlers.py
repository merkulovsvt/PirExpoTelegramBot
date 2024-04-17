from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.data.user_data import get_user_data, post_user_data
from bot.keyboards.user_boards import (inline_start, reply_get_phone_number,
                                       reply_main_menu)
from bot.utils.filters import LoggedOut
from bot.utils.states import User

router = Router()


# Хендлер для команды /start ~
@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    if not await state.get_state():
        user_data = get_user_data(message.chat.id)
        if user_data.get("detail"):
            await state.set_state(User.logged_out)
        else:
            await state.set_state(User.logged_in)

    fsm_user_state = await state.get_state()

    if fsm_user_state == "User:logged_in":
        text, keyboard = reply_main_menu()
        await message.answer(text=text, reply_markup=keyboard)

    elif fsm_user_state == "User:logged_out":
        text, keyboard = reply_get_phone_number()
        await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки команды /info +
@router.message(Command("info"))
async def command_info(message: types.Message):
    text, keyboard = inline_start()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки неверных ответов при регистрации +
@router.message(LoggedOut(), ~F.contact)
async def user_login(message: types.Message):
    text, keyboard = reply_get_phone_number()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки пользовательского номера телефона ~
@router.message(LoggedOut(), F.contact)
async def user_login(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    if phone[0] != "+":
        phone = "+" + phone

    await post_user_data(chat_id=message.chat.id, phone=phone)
    await state.set_state(User.logged_in)

    text, keyboard = reply_main_menu(phone=phone)
    await message.answer(text=text, reply_markup=keyboard)
