from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder


# Inline клавиатура для вывода дат
def inline_timetable_dates(events: dict):
    builder = InlineKeyboardBuilder()

    if events:
        text = "Выберите день:"

        dates = set()
        for event in events:
            if event['time_start']:
                dates.add(datetime.fromisoformat(event["time_start"]).date())

        for date in sorted(dates):
            builder.button(text=date.strftime('%d.%m.%Y'), callback_data=f"timetable_{date}")
    else:
        text = 'К сожалению, у вас нет приобретенных мероприятий'

    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка мероприятий по времени
def inline_timetable_events_list(events: dict, date: str):
    builder = InlineKeyboardBuilder()

    text = f"Мероприятия на {datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m')}"

    event_list = []
    min_name_len = float("inf")
    for event in events:
        event_list.append((event.get('id'), event.get('name'), event.get("time_start"), event.get('time_finish')))
        min_name_len = min(min_name_len, len(event['name']))

    for id, name, time_start, time_finish in sorted(event_list, key=lambda x: x[2]):
        time_start = datetime.fromisoformat(time_start).strftime('%H:%M')
        time_finish = datetime.fromisoformat(time_finish).strftime('%H:%M')

        event_name = name if len(name) < 27 else name[:27] + '...'
        button_text = f"{time_start} - {time_finish} {event_name}"
        builder.button(text=button_text, callback_data=f'time_event_{id}')

    builder.button(text="📅 Вернуться к выбору дня", callback_data="dates_list")
    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода деталей мероприятий
def inline_timetable_events_details(event_data: dict):
    builder = InlineKeyboardBuilder()
    id = event_data.get('id')
    name = event_data.get('name')
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
            f"<b>{type_name}</b>: \"{name}\"\n\n"
            f"<b>Место</b>: {event_data['place'].get('name') if event_data.get('place') else ''}")

    builder.button(text="Скачать билет", callback_data=f"print_event_{ticket_type_id}")
    builder.button(text="📅 Вернуться к списку мероприятий", callback_data=f"timetable_{event_date}")

    builder.adjust(1)
    return text, builder.as_markup()
