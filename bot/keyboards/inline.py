from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.data import User


def inline_start(check: bool) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    if check:
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота!")
    else:
        builder.button(
            text="Регистрация",
            callback_data="login")
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота! Зарегистрируйтесь, "
                "нажав на кнопку.")
    builder.button(
        text="Наш сайт",
        url="https://pirexpo.com/")

    return text, builder.as_markup()


from aiogram.filters.callback_data import CallbackData


class OrderInfo(CallbackData, prefix="order"):
    order_id: int


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

    return text, builder.as_markup()


class TicketInfo(CallbackData, prefix="ticket"):
    order_id: int
    ticket_id: int


def inline_order(order_id: int) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Заказ №{order_id}"

    builder.button(text="Билеты", callback_data=f"tickets_{order_id}")
    # TODO
    builder.button(text="Счет-договор", callback_data="1234")
    builder.button(text="УПД", callback_data="1235")
    # TODO
    builder.button(text="Вернуться к заказам", callback_data="orders")

    builder.adjust(3, 1)

    return text, builder.as_markup()


def inline_tickets(tickets: list, order_id: int) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()

    if tickets:
        text = f"Билеты заказа №{order_id}"
        for ticket_id in tickets:
            builder.button(
                text=f"Билет №{ticket_id}",
                callback_data=TicketInfo(order_id=order_id, ticket_id=ticket_id))
    else:
        text = "К сожалению, у вас нет билетов."

    # TODO
    builder.button(text="Вернуться к заказу", callback_data="41231313")
    # TODO

    return text, builder.as_markup()


def inline_ticket(order_id: int, ticket_id: int) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Билет №{ticket_id}"

    # TODO
    builder.button(text="Редактировать", callback_data="2131223123")
    builder.button(text="Скачать", callback_data="12312312")
    builder.button(text="Информация", callback_data="121231312335")
    builder.button(text="Вернуться к билетам", callback_data="412313131")
    # TODO
    builder.adjust(3, 1)

    return text, builder.as_markup()
