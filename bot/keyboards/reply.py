from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_main():
    buttons = ("Заказы", "Билеты", "Расписание", "Мероприятия", "Экспоненты")
    text = "Вы успешно зарегистрировались!"
    builder = ReplyKeyboardBuilder()
    for elem in buttons:
        builder.add(KeyboardButton(text=elem))
    builder.adjust(1, 2, 2)
    return text, builder.as_markup(resize_keyboard=True)
