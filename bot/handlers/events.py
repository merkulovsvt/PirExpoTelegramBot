from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import event_start_menu
from bot.utils.func_events import load_events
from bot.utils.states import User

router = Router()


# Хэндлер
@router.message(User.logged_in, F.text.lower() == "мероприятия")
async def events_list_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    events = user_data.get("events")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    if not events:
        events = load_events()
        await state.update_data(events=events)

    text, keyboard = event_start_menu()
    await message.answer(text=text, reply_markup=keyboard)

    # if orders:
    #     text, keyboard = inline_orders(orders=orders)
    #     await message.answer(text=text, reply_markup=keyboard)
    # else:
    #     await message.answer(text="К сожалению, у вас нет заказов")
