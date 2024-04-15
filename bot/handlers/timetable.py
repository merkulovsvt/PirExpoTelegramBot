from aiogram import F, Router, types
from aiogram.enums import ParseMode

from bot.data.events_data import get_event_data, get_events_list
from bot.keyboards.timetable_boards import (inline_timetable_dates,
                                            inline_timetable_events_details,
                                            inline_timetable_events_list)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выводу дат мероприятий пользователя по reply кнопке
@router.message(LoggedIn(), F.text.lower() == "📅 расписание")
async def timetable_date_view(message: types.Message):
    events = get_events_list(chat_id=message.chat.id)

    text, keyboard = inline_timetable_dates(events=events)
    if keyboard:
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text=text)


# Хендлер по выводу дат мероприятий пользователя по inline кнопке
@router.callback_query(LoggedIn(), F.data == "dates_list")
async def callback_timetable_date_view(callback: types.CallbackQuery):
    events = get_events_list(chat_id=callback.message.chat.id)

    if events:
        text, keyboard = inline_timetable_dates(events=events)
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text="К сожалению, у вас нет приобретенных мероприятий.")
    await callback.answer()


# Хендлер по выводу списка мероприятия
@router.callback_query(LoggedIn(), F.data.startswith("timetable_"))
async def timetable_events_view(callback: types.CallbackQuery):
    date = callback.data.split("_")[1]
    events = get_events_list(chat_id=callback.message.chat.id, date=date)

    text, keyboard = inline_timetable_events_list(events=events, date=date)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


# Хендлер по выводу деталей мероприятия
@router.callback_query(LoggedIn(), F.data.startswith('time_event_'))
async def timetable_events_data_view(callback: types.CallbackQuery):
    event_id = callback.data.split("_")[2]
    event_data = get_event_data(event_id=event_id)

    text, keyboard = inline_timetable_events_details(event_data=event_data)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
