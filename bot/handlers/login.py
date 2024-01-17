from aiogram import F, Router, types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.login_boards import (inline_start, reply_send_phone_number,
                                        reply_main_menu)
from bot.utils.states import User

router = Router()


# @router.startup()
# async def notify_message(dp: Dispatcher):
    # last_state = await state.get_state()
    # await state.set_state(User.logged_out)
    # cur_state = await state.get_state()
    # print(cur_state)
    # await state.set_state()
    # cur_state = await state.get_state()
    # print(cur_state)
    # await state.set_state(last_state)
    # return


# Хендлер для команды /start +
@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    text, keyboard = inline_start()
    await message.answer(text=text, reply_markup=keyboard)

    user_data = await state.get_data()

    if not user_data:
        await state.set_state(User.logged_out)
        text, keyboard = reply_send_phone_number()
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await state.set_state(User.logged_in)
        text, keyboard = reply_main_menu(phone=user_data['phone'])
        await message.answer(text=text, reply_markup=keyboard)


# Хендлер для обработки неверных ответов при регистрации +
@router.message(User.logged_out, ~F.contact)
async def user_login(message: types.Message):
    await message.answer(text="Зарегистрируйтесь, поделившись с нами номером вашего телефона")


# Хендлер для обработки пользовательского номера телефона +
@router.message(User.logged_out, F.contact)
async def user_login(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    await state.set_state(User.logged_in)
    await state.update_data(phone=phone)

    text, keyboard = reply_main_menu(phone=phone)
    await message.answer(text=text, reply_markup=keyboard)
