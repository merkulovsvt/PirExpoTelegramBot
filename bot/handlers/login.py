from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import inline_start
from bot.keyboards.reply import reply_main
from bot.utils.states import User

router = Router()


# Хэндлер /start ?
@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data:
        await state.set_state(User.logged_out)

    text, keyboard = inline_start(user_data)
    await message.answer(text, reply_markup=keyboard)


# Хэндлер по извлечению номера телефона из сообщения ?
@router.callback_query(User.logged_out, F.data == "registration")
async def callback_user_login(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите ваш номер телефона, что вы указывали при покупке билетов. В формате +79161754807:")
    await state.set_state(User.registrating)
    await callback.answer()


# Хэндлер по извлечению номера телефона из сообщения ?
@router.message(User.registrating)
async def user_login(message: types.Message, state: FSMContext):
    entities = message.entities or []

    if len(entities) == 1 and entities[0].type == 'phone_number':
        phone = entities[0].extract_from(message.text)

        await state.update_data(phone=phone)
        await state.set_state(User.logged_in)

        text, keyboard = reply_main(phone=phone)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.reply("Некорректный формат данных.")
