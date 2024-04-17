from aiogram.filters.callback_data import CallbackData


class TimetableEventsList(CallbackData, prefix="timetable_events"):
    event_date: str
