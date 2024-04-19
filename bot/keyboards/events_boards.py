from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.events_callbacks import (EventDetails, EventPrint,
                                            EventsList, EventsThemes)
from bot.callbacks.timetable_callbacks import TimetableEventsList


# Inline клавиатура для выбора категории мероприятий (Мои/Все)
def inline_event_categories():
    builder = InlineKeyboardBuilder()
    text = "Выберите категорию:"

    builder.button(text="Мои мероприятия", callback_data=EventsThemes(events_type='my'))
    builder.button(text="Все мероприятия", callback_data=EventsThemes(events_type='*'))

    return text, builder.as_markup()


# Inline клавиатура для выбора темы мероприятия
def inline_events_themes(event_themes: dict, events_type: str):
    builder = InlineKeyboardBuilder()

    themes_set = set()
    for theme in event_themes.get("theme"):
        themes_set.add((theme['name'], str(theme['id'])))

    if len(themes_set) == 0:
        if events_type == "my":
            text = "К сожалению, у вас нет приобретенных мероприятий."
        else:
            text = "К сожалению, не можем вывести список тем."

    else:
        text = "Темы мероприятий:"
        for theme in sorted(themes_set):
            button_text = f"{theme[0]}"
            if events_type == "my":
                builder.button(text=button_text, callback_data=EventsList(theme_id=theme[1]))
            else:
                builder.button(text=button_text, url=f'https://pirexpo.com/program/schedule?theme={theme[1]}')

    builder.button(text="🎉 Вернуться к выбору категории мероприятий", callback_data="event_categories_list")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка мероприятий
def inline_events_list(events: dict, theme_id: str):
    builder = InlineKeyboardBuilder()

    text = f"Мероприятия {events[0]['theme']['name']}"

    events_set = set()
    min_name_len = float("inf")
    for event in events:
        events_set.add((event.get('id'), event.get('name').strip('\"')))
        min_name_len = min(min_name_len, len(event.get('name').strip('\"')))

    for id, name in sorted(events_set, key=lambda x: len(x[1])):

        n_chars = 7
        if len(name) > min_name_len:
            if len(name) - min_name_len > n_chars:
                event_name = name[:min_name_len + n_chars] + '...'
            else:
                event_name = name[:min_name_len] + '...'
        else:
            event_name = name

        button_text = event_name
        builder.button(text=button_text, callback_data=EventDetails(theme_id=theme_id, event_id=str(id)))

    builder.button(text="🎉 Вернуться к выбору темы мероприятий", callback_data=EventsThemes(events_type="my"))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода деталей мероприятия
def inline_events_details(event_data: dict, theme_id: str):
    builder = InlineKeyboardBuilder()
    event_name = event_data.get('name').strip("\"")
    type_name = event_data.get('type').get('name')
    ticket_type_id = event_data.get('ticket_type').get('id')
    time_start = event_data.get("time_start")
    time_finish = event_data.get('time_finish')

    date = datetime.fromisoformat(time_start).strftime('%d.%m.%Y')
    event_date = datetime.fromisoformat(time_start).strftime('%Y-%m-%d')
    time_start = datetime.fromisoformat(time_start).strftime('%H:%M')
    time_finish = datetime.fromisoformat(time_finish).strftime('%H:%M')

    text = (f"<b>Дата:</b> <i>{date}</i>\n\n"
            f"<b>Время:</b> <i>{time_start}</i> - <i>{time_finish}</i>\n\n"
            f"<b>{type_name}</b>: \"{event_name}\"\n\n"
            f"<b>Место</b>: {event_data.get('place').get('name') if event_data.get('place') else ''}")

    text = text.replace("<br>", "\n")

    builder.button(text="Скачать билет", callback_data=EventPrint(ticket_type_id=str(ticket_type_id)))

    if theme_id == "*":
        builder.button(text="📅 Вернуться к списку билетов", callback_data=TimetableEventsList(event_date=event_date))
    else:
        builder.button(text="🎉 Вернуться к списку билетов", callback_data=EventsList(theme_id=theme_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()
