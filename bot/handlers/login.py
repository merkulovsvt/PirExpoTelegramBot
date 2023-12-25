from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import inline_start
from bot.keyboards.reply import reply_main
from bot.data import User

router = Router()


@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data:
        await state.set_state(User.logged_out)
    await message.answer(inline_start(bool(user_data))[0], reply_markup=inline_start(bool(user_data))[1])


@router.callback_query(User.logged_out, F.data == "login")
async def callback_user_login(callback: types.CallbackQuery):
    await callback.message.answer(
        "Введите ваш номер телефона, что вы указывали при покупке билетов. В формате +79161754807:")
    await callback.answer()


@router.message(User.logged_out)
async def user_login(message: types.Message, state: FSMContext):
    entities = message.entities or []
    if len(entities) == 1 and entities[0].type == 'phone_number':
        await state.update_data(phone=entities[0].extract_from(message.text))
        await state.set_state(User.logged_in)
        await message.answer(
            "Вы успешно зарегистрировались!",
            reply_markup=reply_main()
        )
    else:
        await message.reply("Некорректный формат данных.")
