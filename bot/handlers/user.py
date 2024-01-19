from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.data.user_data import put_user_data, get_user_data
from bot.keyboards.user_boards import (inline_start, reply_get_phone_number,
                                       reply_main_menu)
from bot.utils.filters import LoggedIn, LoggedOut
from bot.utils.states import User

router = Router()


# Хендлер для команды /start ~
@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    if not await state.get_state():
        server_user_state = get_user_data(message.chat.id)["state"]
        if not server_user_state:
            await put_user_data(chat_id=message.chat.id, state="User:logged_out")
            await state.set_state(User.logged_out)
        elif server_user_state == "User:logged_in":
            await state.set_state(User.logged_in)
        elif server_user_state == "User:logged_out":
            await state.set_state(User.logged_out)

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
async def user_login(message: types.Message, state: FSMContext):
    print(await state.get_state())
    text, keyboard = reply_get_phone_number()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки пользовательского номера телефона ~
@router.message(LoggedOut(), F.contact)
async def user_login(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number

    if phone_number[0] != "+":
        phone_number = "+" + phone_number

    await put_user_data(chat_id=message.chat.id, state="User:logged_in", phone_number=phone_number)
    await state.set_state(User.logged_in)

    print(await state.get_state())

    text, keyboard = reply_main_menu(phone_number=phone_number)
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки команды /logout ~
@router.message(LoggedIn(), Command("logout"))
async def logout(message: types.Message, state: FSMContext):
    await message.answer("Вы успешно вышли из системы", reply_markup=ReplyKeyboardRemove())
    await message.answer("/start")
    # message = types.Message(text="/start")

    # Process the simulated command
    # await message.process_commands(types.Message(text="/start"))

    await put_user_data(chat_id=message.chat.id, state="User:logged_out", phone_number="*")
    await state.set_state(User.logged_out)
