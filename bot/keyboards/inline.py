from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo, TicketInfo


# Клавиатура для start меню +
def inline_start(check: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    if check:
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота!")
    else:
        builder.button(
            text="Регистрация",
            callback_data="registration")
        text = ("Добро пожаловать в нашего бота! Мы - компания Пир Экспо, занимаемся организацией выставок в сфере "
                "гостеприимства. У нас вы найдете самые актуальные и интересные мероприятия, которые помогут вам "
                "развиваться и находить новых партнеров. Приятного использования нашего бота! Зарегистрируйтесь, "
                "нажав на кнопку.")
    builder.button(
        text="Наш сайт",
        url="https://pirexpo.com/")

    return text, builder.as_markup()


# Клавиатура для вывода списка заказов +
def inline_orders(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()

    text = "Ваши заказы:"
    for order_id in orders:
        builder.button(
            text=f"Заказ №{order_id}",
            callback_data=OrderInfo(order_id=order_id))
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Клавиатура для вывода данных заказа
def inline_order_data(order_id: int, is_invoice: bool) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Заказ №{order_id}"

    builder.button(text="Билеты", callback_data=f"ticket_types_{order_id}")

    if is_invoice:
        builder.button(text="Счет-договор", callback_data=f"invoice_{order_id}")
        # TODO
        builder.button(text="УПД", callback_data="1235")
        builder.button(text="Вернутся к заказам", callback_data="orders")
        builder.adjust(1, 2, 1)
    else:
        builder.button(text="Вернутся к заказам", callback_data="orders")
        builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Клавиатура для выбора типа билета +
def inline_ticket_types(from_order: bool, order_id=-1) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип билета"

    if from_order:
        builder.button(text="Входные билеты", callback_data=f"tickets_entry_{order_id}")
        builder.button(text="Мероприятия", callback_data=f"tickets_event_{order_id}")
        builder.button(text="Вернуться к заказу", callback_data=OrderInfo(order_id=order_id))
        builder.adjust(2, 1)
    else:
        builder.button(text="Входные билеты", callback_data=f"tickets_entry_*")
        builder.button(text="Мероприятия", callback_data=f"tickets_event_*")
        builder.adjust(2)

    return text, builder.as_markup()


# Клавиатура для вывода списка билетов +
def inline_tickets_list(tickets_list: list, ticket_type: str, from_order: bool, order_id=-1):
    text = ""
    builder = InlineKeyboardBuilder()

    if ticket_type == "entry":
        text = "Входные билеты:"
    elif ticket_type == "event":
        text = "Билеты на мероприятия:"

    if tickets_list:
        for ticket_id in tickets_list:
            builder.button(
                text=f"Билет №{ticket_id}",
                callback_data=TicketInfo(order_id=order_id, from_order=from_order, ticket_id=ticket_id,
                                         ticket_type=ticket_type))
    else:
        text = "К сожалению, у вас нет билетов в данной категории"

    if from_order:
        callback_data = f"ticket_types_{order_id}"
    else:
        callback_data = f"ticket_types_*"

    builder.button(text="Вернуться к выбору категории", callback_data=callback_data)
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Клавиатура для вывода данных билета +
def inline_ticket_data(order_id: int, from_order: bool, ticket_id: int, ticket_type: str):
    text = ""
    builder = InlineKeyboardBuilder()

    builder.button(text="Скачать", callback_data=f"print_ticket_{ticket_id}")
    # TODO
    builder.button(text="?Вернуть?", callback_data="111")
    if ticket_type == "entry":
        text = f"Входной билет №{ticket_id}"
        # TODO
        builder.button(text="Редактировать", url="zaza.com")  # Ждём ссылку от Леши

    elif ticket_type == "event":
        text = f"Билет на мероприятие №{ticket_id}"
        # TODO
        builder.button(text="Информация о мероприятии", callback_data="121231312335")

    if from_order:
        addon = order_id
    else:
        addon = "*"

    builder.button(text="Вернуться к списку билетов", callback_data=f"tickets_{ticket_type}_{addon}")

    builder.adjust(2, 1, 1)

    return text, builder.as_markup()
