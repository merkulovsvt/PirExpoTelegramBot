from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo


# Inline клавиатура для вывода списка заказов +
def inline_orders_list(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = "Ваши заказы:"

    for order_id in orders:
        order_date = datetime.strptime(orders[order_id]['order_date'], "%Y-%m-%d")
        builder.button(text=f"Заказ №{order_id} от {order_date.strftime('%d.%m.%Y')}",
                       callback_data=OrderInfo(order_id=order_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода деталей заказа ~
def inline_order_details(order_id: str, order_details: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Детали заказа №{order_id}"

    builder.button(text="🎫 Билеты", callback_data=f"tickets_*_{order_id}")

    if order_details.get("invoice_url"):
        builder.button(text="Счет-договор", callback_data=f"invoice_print_{order_id}")
        builder.button(text="УПД", callback_data="1235")  # Доделать
        builder.adjust(1, 2, 1)
    else:
        builder.adjust(1, repeat=True)
    builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
    return text, builder.as_markup()
