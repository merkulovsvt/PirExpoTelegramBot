from aiogram import F, Router, types

from bot.data.events_data import get_events_list
from bot.keyboards.events_boards import inline_event_types, inline_events_themes, inline_events_list
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выбору типа мероприятий по reply кнопке
@router.message(LoggedIn(), F.text.lower() == "🎉 мероприятия")
async def events_type_view(message: types.Message):
    text, keyboard = inline_event_types()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выбору типа мероприятий по inline кнопке
@router.callback_query(LoggedIn(), F.data == "event_types")
async def callback_events_type_view(callback: types.CallbackQuery):
    text, keyboard = inline_event_types()
    await callback.message.edit_text(text=text, reply_markup=keyboard)


# Хендлер по выбору тематик мероприятия
@router.callback_query(LoggedIn(), F.data.startswith("event_themes_"))
async def callback_events_theme_view(callback: types.CallbackQuery):
    events_type = callback.data.split("_")[2]

    if events_type == "my":
        events = get_events_list(chat_id=callback.message.chat.id)
    else:
        events = get_events_list()

    text, keyboard = inline_events_themes(events=events, events_type=events_type)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


# Хендлер по выводу списка мероприятия
@router.callback_query(LoggedIn(), F.data.startswith("events_"))
async def callback_events_list_view(callback: types.CallbackQuery):
    events_type = callback.data.split("_")[1]
    theme_id = callback.data.split("_")[2]

    print(callback.data.split("_"))

    if events_type == "my":
        events = get_events_list(chat_id=callback.message.chat.id)
    else:
        events = get_events_list()

    print(events)

    text, keyboard = inline_events_list(events=events, events_type=events_type, theme_id=theme_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
