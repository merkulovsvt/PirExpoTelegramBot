from aiogram.utils.keyboard import InlineKeyboardBuilder


def event_start_menu():
    builder = InlineKeyboardBuilder()

    text = "Выберите кнопку"
    builder.button(text="Мои мероприятия", callback_data="zaza1")
    builder.button(text="Все мероприятия", callback_data="zaza1")
    builder.button(text="Бесплатные мероприятия", callback_data="zaza1")
    return text, builder.as_markup()
