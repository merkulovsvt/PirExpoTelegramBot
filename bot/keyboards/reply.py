from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Основная reply клавиатура ?
def reply_main(phone: str):
    buttons = ("Заказы", "Билеты", "Расписание", "Мероприятия", "Экспоненты")
    text = f"Вы успешно зарегистрировались по номеру {phone}!"
    builder = ReplyKeyboardBuilder()
    for elem in buttons:
        builder.add(KeyboardButton(text=elem))
    builder.adjust(1, 2, 2)
    return text, builder.as_markup(resize_keyboard=True)
