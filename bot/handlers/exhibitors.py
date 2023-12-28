from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot.utils.func_exhibitors import load_exhibitors
from bot.utils.states import User

router = Router()


# Хэндлер по выводу списка заказов по reply кнопке +
@router.message(User.logged_in, F.text.lower() == "экспоненты")
async def exhibitor_list_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    exhibitors = user_data.get("exhibitors")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    if not exhibitors:
        exhibitors = load_exhibitors()
        await state.update_data(exhibitors=exhibitors)

    await message.answer(text="i have the data")

    # if orders:
    #     text, keyboard = inline_orders(orders=orders)
    #     await message.answer(text=text, reply_markup=keyboard)
    # else:
    #     await message.answer(text="К сожалению, у вас нет заказов")
