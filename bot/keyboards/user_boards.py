from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.utils.config import exhibition_url, bot_start_text, exhibition_name


# Inline клавиатура для /start +
def inline_start() -> (str, InlineKeyboardBuilder):
    builder = InlineKeyboardBuilder()
    builder.button(text="Наш сайт", url=exhibition_url)

    start_text = bot_start_text

    return start_text, builder.as_markup()


# Reply клавиатура для отправки номера телефона пользователем +
def reply_get_phone_number() -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='📞 Поделиться номером телефон', request_contact=True))

    text = "Зарегистрируйтесь, поделившись с нами вашим номером телефона 📞:"
    return text, builder.as_markup(resize_keyboard=True)


# Reply клавиатура для основного меню +
def reply_main_menu(phone=None) -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()

    if exhibition_name == 'PIR':
        buttons = ("🛒 Заказы", "🎫 Билеты", "🎉 Мероприятия", "📅 Расписание", "🤝 Экспоненты", "🤝 Партнёры")
    else:
        buttons = ("🛒 Заказы", "🎫 Билеты", "📍 План мероприятия", "🎉 Расписание", "🤝 Экспоненты", "🤝 Партнёры")

    for elem in buttons:
        builder.add(KeyboardButton(text=elem))
    builder.adjust(2, 2, 2)

    start_text = bot_start_text

    if phone:
        text = f"Вы успешно зарегистрировались по номеру {phone}!\n"
    else:
        text = start_text

    return text, builder.as_markup(resize_keyboard=True)
