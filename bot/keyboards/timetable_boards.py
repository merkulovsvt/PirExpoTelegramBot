from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder


# Inline клавиатура для вывода дат
def inline_timetable_dates(events: dict):
    builder = InlineKeyboardBuilder()
    text = "Выберите день:"

    dates = set()
    for event in events:
        if event['time_start']:
            dates.add(datetime.fromisoformat(event["time_start"]).date())

    for date in sorted(dates):
        builder.button(text=date.strftime('%d.%m.%Y'), callback_data=f"timetable_{date}")

    builder.adjust(1)
    return text, builder.as_markup()


def inline_timetable_events_list(event: dict, date: str):
    builder = InlineKeyboardBuilder()

    time_start = datetime.fromisoformat(event["time_start"]).strftime('%H:%M')
    time_finish = datetime.fromisoformat(event["time_finish"]).strftime('%H:%M')

    text = (f"<b>Дата:</b> <i>{datetime.fromisoformat(date).strftime('%d.%m.%Y')}</i>\n\n"
            f"<b>Время:</b> <i>{time_start}</i> - <i>{time_finish}</i>\n\n"
            f"<b>{event['type']['name']}</b>: \"{event.get('name')}\"\n\n"
            f"<b>Место</b>: {event['place'].get('name') if event.get('place') else ''}")

    builder.button(text="Скачать билет", callback_data=f"print_event_{event['ticket_type']['id']}")

    builder.adjust(1)
    return text, builder.as_markup()
