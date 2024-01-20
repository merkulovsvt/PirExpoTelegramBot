from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_event_types():
    builder = InlineKeyboardBuilder()

    text = "Выберите категорию:"
    builder.button(text="Мои мероприятия", callback_data="event_themes_my")
    builder.button(text="Все мероприятия", callback_data="event_themes_all")
    return text, builder.as_markup()


def inline_events_themes(events: dict, events_type: str):
    builder = InlineKeyboardBuilder()
    themes = set()

    for event in events:
        themes.add((event['theme']['name'], event['theme']['id']))

    if len(themes) == 0:
        text = "К сожалению, у вас нет приобретенных мероприятий."

    else:
        text = "Темы мероприятий:"
        for theme in sorted(themes):
            button_text = f"{theme[0]}"
            builder.button(text=button_text, callback_data=f"events_{events_type}_{theme[1]}")

    builder.button(text="Вернуться к выбору типа мероприятий", callback_data="event_types")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


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
