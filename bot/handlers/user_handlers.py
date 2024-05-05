from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.data.user_data import get_user_data, post_user_data
from bot.keyboards.user_boards import reply_get_phone_number, reply_main_menu
from bot.utils.config import bot_start_text
from bot.utils.filters import CheckReady, LoggedOut
from bot.utils.states import User

router = Router()


# Хендлер для команды /start (регистрации)
@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    if not await state.get_state():
        user_data = await get_user_data(chat_id=message.chat.id)

        if user_data:
            await state.set_state(User.logged_in)
        else:
            await state.set_state(User.logged_out)

    fsm_user_state = await state.get_state()

    if fsm_user_state == "User:logged_in":
        text, keyboard = reply_main_menu()
        await message.answer(text=text, reply_markup=keyboard)

    elif fsm_user_state == "User:logged_out":
        await message.answer(text=bot_start_text)
        text, keyboard = reply_get_phone_number()
        await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки пользовательского номера телефона
@router.message(LoggedOut(), F.contact)
async def user_login(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    if phone[0] != "+":
        phone = "+" + phone

    await post_user_data(chat_id=message.chat.id, phone=phone)
    await state.set_state(User.logged_in)

    text, keyboard = reply_main_menu(phone=phone)
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки неверных ответов при регистрации
@router.message(LoggedOut(), ~F.contact)
async def wrong_user_login(message: types.Message):
    text, keyboard = reply_get_phone_number()
    await message.answer(text=text, reply_markup=keyboard)


ignore_text = ["🛒 заказы", "🎫 билеты", "📅 расписание", "🎉 мероприятия", "🤝 экспоненты", "🤝 партнёры"]


# Хендлер для обработки неверных ответов после регистрации
@router.message(CheckReady(), ~F.text.lower().in_(ignore_text))
async def incorrect_user_message(message: types.Message):
    text = ('К сожалению я не смог распознать Вашу команду.\n'
            'Воспользуйтесь кнопками в меню или отправьте /start')
    _, keyboard = reply_main_menu()

    await message.answer(text=text, reply_markup=keyboard)
