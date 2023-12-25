from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_start(check: bool) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    if check:
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота!")
    else:
        builder.add(InlineKeyboardButton(
            text="Регистрация",
            callback_data="login"))
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота! Зарегистрируйтесь, "
                "нажав на кнопку.")
    builder.add(InlineKeyboardButton(
        text="Наш сайт",
        url="https://pirexpo.com/"))

    return text, builder.as_markup()
