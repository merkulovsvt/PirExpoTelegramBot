from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo, TicketInfo
from bot.utils.config import User


# Клавиатура для start меню
def inline_start(check: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    if check:
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота!")
    else:
        builder.button(
            text="Регистрация",
            callback_data="register")
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота! Зарегистрируйтесь, "
                "нажав на кнопку.")
    builder.button(
        text="Наш сайт",
        url="https://pirexpo.com/")

    return text, builder.as_markup()


# Клавиатура для вывода списка заказов
def inline_orders(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()

    if orders:
        text = "Ваши заказы:"
        for order_id in orders:
            builder.button(
                text=f"Заказ №{order_id}",
                callback_data=OrderInfo(order_id=order_id))
    else:
        text = "К сожалению, у вас нет заказов."

    return text, builder.as_markup(row_width=1)


# Клавиатура для вывода данных заказа
def inline_order_data(order_id: int) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Заказ №{order_id}"

    builder.button(text="Билеты", callback_data=f"tickets_{order_id}")
    builder.button(text="Счет-договор", callback_data=f"invoice_{order_id}")

    # TODO
    builder.button(text="УПД", callback_data="1235")
    builder.button(text="Вернутся к заказам", callback_data="orders")
    # TODO

    builder.adjust(1, 2, 1)

    return text, builder.as_markup()


# Клавиатура для вывода списка билетов
def inline_tickets(order_ids, ticket_ids: list) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    if ticket_ids:
        if isinstance(order_ids, int):
            text = f"Билеты заказа №{order_ids}"
            for ticket_id in ticket_ids:
                builder.button(
                    text=f"Билет №{ticket_id}",
                    callback_data=TicketInfo(order_id=order_ids, ticket_id=ticket_id, from_order=True))
            builder.button(text="Вернуться к заказу", callback_data=OrderInfo(order_id=order_ids))
        else:
            text = "Ваши билеты"
            for order_id, ticket_id in zip(order_ids, ticket_ids):
                builder.button(
                    text=f"Билет №{ticket_id}",
                    callback_data=TicketInfo(order_id=order_id, ticket_id=ticket_id, from_order=False))
    else:
        text = "К сожалению, у вас нет билетов."

    return text, builder.as_markup(row_width=1)


# Клавиатура для вывода данных билета
def inline_ticket_data(order_id: int, ticket_id: int, from_order: bool) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Билет №{ticket_id}"

    builder.button(text="Скачать", callback_data=f"print_ticket_{ticket_id}")

    # TODO
    builder.button(text="Редактировать", url="zaza.com")  # Ждём ссылку от Леши
    builder.button(text="Информация", callback_data="121231312335")
    # TODO

    if from_order:
        addon = order_id
    else:
        addon = "*"

    builder.button(text="Вернуться к билетам", callback_data=f"tickets_{addon}")

    builder.adjust(3, 1)

    return text, builder.as_markup()
