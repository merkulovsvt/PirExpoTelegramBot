from aiogram import F, Router, types
from aiogram.enums import ChatAction

from bot.callbacks.timetable_callbacks import TimetableEventsList
from bot.data.events_data import get_events_list
from bot.keyboards.timetable_boards import (inline_timetable_dates_list,
                                            inline_timetable_events_list)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выводу дат мероприятий по reply кнопке
@router.message(LoggedIn(), F.text.lower() == "📅 расписание")
async def timetable_dates_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    events = await get_events_list(chat_id=message.chat.id, event_date=None, theme_id=None)

    text, keyboard = inline_timetable_dates_list(events=events)
    if keyboard:
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text=text)


# Хендлер по выводу дат мероприятий по inline кнопке
@router.callback_query(LoggedIn(), F.data == "timetable_dates_list")
async def callback_timetable_dates_view(callback: types.CallbackQuery):
    events = await get_events_list(chat_id=callback.message.chat.id, event_date=None, theme_id=None)

    if events:
        text, keyboard = inline_timetable_dates_list(events=events)
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text="К сожалению, у вас нет приобретенных мероприятий.")
    await callback.answer()


# Хендлер по выводу списка мероприятия
@router.callback_query(LoggedIn(), TimetableEventsList.filter())
async def timetable_events_view(callback: types.CallbackQuery, callback_data: TimetableEventsList):
    event_date = callback_data.event_date

    events = await get_events_list(chat_id=callback.message.chat.id, event_date=event_date, theme_id=None)

    text, keyboard = inline_timetable_events_list(events=events, event_date=event_date)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()
