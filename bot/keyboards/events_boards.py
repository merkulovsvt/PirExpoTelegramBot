from aiogram.utils.keyboard import InlineKeyboardBuilder


# Inline клавиатура для выбора категории
def inline_event_categories():
    builder = InlineKeyboardBuilder()
    text = "Выберите категорию:"

    builder.button(text="Мои мероприятия", callback_data="event_themes_my")
    builder.button(text="Все мероприятия", callback_data="event_themes_all")
    return text, builder.as_markup()


# Inline клавиатура для выбора темы мероприятия
def inline_events_themes(event_themes: dict, events_type: str):
    builder = InlineKeyboardBuilder()

    themes_set = set()
    for theme in event_themes["theme"]:
        themes_set.add((theme['name'], theme['id']))

    if len(themes_set) == 0:
        text = "К сожалению, у вас нет приобретенных мероприятий."

    else:
        text = "Темы мероприятий:"
        for theme in sorted(themes_set):
            button_text = f"{theme[0]}"
            builder.button(text=button_text, callback_data=f"events_{events_type}_{theme[1]}")

    builder.button(text="Вернуться к выбору категории мероприятий", callback_data="event_categories")

    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для выбора площадки мероприятия
def inline_events_areas(events: dict, events_type: str, theme_id: str):
    builder = InlineKeyboardBuilder()
    text = f"Мероприятия тематики {theme_id}"

    for event in events:
        if event['theme']['id'] == int(theme_id):
            button_text = f"{event['name']}"
            builder.button(text=button_text, callback_data=f"zaza")

    builder.button(text="Вернуться к выбору темы мероприятий", callback_data=f"event_themes_{events_type}")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка мероприятий
def inline_events_list(events: dict, events_type: str, theme_id: str):
    builder = InlineKeyboardBuilder()
    text = f"Мероприятия тематики {theme_id}"

    for event in events:
        if event['theme']['id'] == int(theme_id):
            print(event["thematics"])
            button_text = f"{event['name']}"
            builder.button(text=button_text, callback_data=f"zaza")

    builder.button(text="Вернуться к выбору темы мероприятий", callback_data=f"event_themes_{events_type}")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()

def inline_events_details(event: dict, date: str):
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



# def inline_events_details(event_details: dict, events_type: str, theme_id: str):
#     builder = InlineKeyboardBuilder()
#     text = f"Мероприятия тематики {theme_id}"
#
#     for event in events:
#         if event['theme']['id'] == int(theme_id):
#             print(event["thematics"])
#             button_text = f"{event['name']}"
#             builder.button(text=button_text, callback_data=f"zaza")
#
#     builder.button(text="Вернуться к выбору темы мероприятий", callback_data=f"event_themes_{events_type}")
#
#     builder.adjust(1, repeat=True)
#     return text, builder.as_markup()
