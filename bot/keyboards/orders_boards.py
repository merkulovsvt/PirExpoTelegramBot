from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.orders_data import tickets_status_check
from bot.utils.callbackdata import OrderInfo


# Inline клавиатура для вывода списка заказов +
def inline_orders_list(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()

    orders_list = []
    for order in orders:
        if order["status"] == 3 and tickets_status_check(order=order):
            date = datetime.fromisoformat(order['date']).strftime('%d.%m.%Y')
            orders_list.append((date, order["id"], order["sum"]))

    if orders_list:
        text = "Ваши заказы:"

        for order in sorted(orders_list, key=lambda x: x[0]):
            button_text = f"Заказ №{order[1]} от {order[0]} на сумму {order[2]}"
            builder.button(text=button_text, callback_data=OrderInfo(order_id=str(order[1])))
    else:
        text = "К сожалению, у вас нет заказов"

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода деталей заказа ~
def inline_order_details(order_id: str, order_details: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Детали заказа №{order_id}:"

    if order_details["status"] == 3:
        builder.button(text="🎫 Билеты", callback_data=f"tickets_*_{order_id}")
        builder.button(text="Возврат", url=order_details["return_request_url"])
        if order_details.get("invoice_pdf_url"):
            builder.button(text="Счет-договор", callback_data=f"invoice_print_{order_id}")
            builder.button(text="УПД", callback_data="1235")  # Доделать
            builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
            builder.adjust(1, 2, 1)
        else:
            builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
            builder.adjust(1, repeat=True)

    return text, builder.as_markup()
