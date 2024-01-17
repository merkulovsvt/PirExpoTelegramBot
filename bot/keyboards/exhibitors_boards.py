from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# Reply клавиатура для отмены поиска экспонентов +
def reply_stop_exhibitors_search() -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    buttons = "Отменить поиск"
    builder.add(KeyboardButton(text=buttons))

    text = f"Вы вернулись в главное меню!"
    return text, builder.as_markup(resize_keyboard=True)


# Inline клавиатура для меню поиска экспонентов +
def inline_exhibitors_search_menu(first_launch: bool):
    builder = InlineKeyboardBuilder()

    text = "Это меню поиска экспонентов. Нажмите на кнопку для продолжения."
    if first_launch:
        builder.button(text="Начать поиск", callback_data="search_exhibitor")
    else:
        builder.button(text="Продолжить поиск?", callback_data="search_exhibitor")
        builder.button(text="Отменить поиск", callback_data="stop_search_exhibitor")
    return text, builder.as_markup()
