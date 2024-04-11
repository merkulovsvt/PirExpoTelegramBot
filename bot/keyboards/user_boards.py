from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# Inline клавиатура для /start +
def inline_start() -> (str, InlineKeyboardBuilder):
    builder = InlineKeyboardBuilder()
    builder.button(text="Наш сайт", url="https://pirexpo.com/")

    text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
            "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
            "развиваться и находить новых партнеров. Приятного использования нашего бота!")
    return text, builder.as_markup()


# Reply клавиатура для отправки номера телефона пользователем +
def reply_get_phone_number() -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=' 📞 Поделиться номером телефон', request_contact=True))

    text = "Зарегистрируйтесь, поделившись с нами вашим номером телефона:"
    return text, builder.as_markup(resize_keyboard=True)


# Reply клавиатура для основного меню +
def reply_main_menu(phone=None) -> (str, ReplyKeyboardBuilder):
    builder = ReplyKeyboardBuilder()
    buttons = ("🛒 Заказы", "🎫 Билеты", "📅 Расписание", "🎉 Мероприятия", "🤝 Экспоненты", "🤝 Партнёры")

    for elem in buttons:
        builder.add(KeyboardButton(text=elem))
    builder.adjust(2, 2, 2)

    if phone:
        text = f"Вы успешно зарегистрировались по номеру {phone}!"
    else:
        text = f"Вы уже вошли в систему!"

    return text, builder.as_markup(resize_keyboard=True)
