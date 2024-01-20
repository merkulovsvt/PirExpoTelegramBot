from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo


# Inline клавиатура для вывода списка заказов +
def inline_orders_list(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = "Ваши заказы:"

    for order in orders:
        button_text = (f"Заказ №{order['id']} от {datetime.fromisoformat(order['date']).strftime('%d.%m.%Y')} "
                       f"на сумму {order['sum']}")
        builder.button(text=button_text if order['status'] == 3 else "Ожидает оплаты " + button_text,
                       callback_data=OrderInfo(order_id=str(order['id'])))

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

    elif order_details["status"] == 2:
        builder.button(text="Оплатить заказ", url="zaza.com")  # Доделать
        builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
        builder.adjust(1, repeat=True)

    return text, builder.as_markup()
