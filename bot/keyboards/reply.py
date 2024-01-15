from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Клавиатура для отправки номера телефона пользователем +
def reply_get_phone_number() -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text='Поделиться номером телефон',
        request_contact=True))

    text = "Зарегистрируйтесь, поделившись с нами вашим номером телефона:"
    return text, builder.as_markup(resize_keyboard=True)


# Клавиатура для основного меню +
def reply_main_menu(phone: str) -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    buttons = ("Заказы", "Билеты", "Расписание", "Мероприятия", "Экспоненты")

    for elem in buttons:
        builder.add(KeyboardButton(text=elem))
    builder.adjust(1, 2, 2)

    text = f"Вы успешно зарегистрировались по номеру {phone}!"
    return text, builder.as_markup(resize_keyboard=True)


# Клавиатура для отмены поиска экспонентов +
def reply_stop_exhibitors_search() -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    buttons = "Отменить поиск"
    builder.add(KeyboardButton(text=buttons))

    text = f"Вы вернулись в главное меню!"
    return text, builder.as_markup(resize_keyboard=True)
