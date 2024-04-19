from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.events_callbacks import EventDetails
from bot.callbacks.timetable_callbacks import TimetableEventsList


# Inline клавиатура для вывода списка дат
def inline_timetable_dates_list(events: dict):
    builder = InlineKeyboardBuilder()

    if events:
        text = "Выберите день:"

        dates_set = set()
        for event in events:
            if event['time_start']:
                dates_set.add(datetime.fromisoformat(event["time_start"]).date())

        for date in sorted(dates_set):
            event_date = str(date)
            builder.button(text=date.strftime('%d.%m.%Y'), callback_data=TimetableEventsList(event_date=event_date))
    else:
        text = 'К сожалению, у вас нет приобретенных мероприятий'

    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка мероприятий
def inline_timetable_events_list(events: dict, event_date: str):
    builder = InlineKeyboardBuilder()

    text = f"Мероприятия на {datetime.strptime(event_date, '%Y-%m-%d').strftime('%d.%m')}"

    events_set = set()
    min_name_len = float("inf")
    for event in events:
        events_set.add((event.get('id'), event.get('name'), event.get("time_start"), event.get('time_finish')))
        min_name_len = min(min_name_len, len(event['name']))

    for id, name, time_start, time_finish in sorted(events_set, key=lambda x: x[2]):
        time_start = datetime.fromisoformat(time_start).strftime('%H:%M')
        time_finish = datetime.fromisoformat(time_finish).strftime('%H:%M')

        event_name = name.strip("\"") if len(name.strip("\"")) < 27 else name.strip("\"")[:27] + '...'
        button_text = f"{time_start} - {time_finish} {event_name}"

        builder.button(text=button_text, callback_data=EventDetails(theme_id='*', event_id=str(id)))

    builder.button(text="📅 Вернуться к выбору дня", callback_data="timetable_dates_list")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()
