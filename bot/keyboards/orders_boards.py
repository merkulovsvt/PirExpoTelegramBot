from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo


# Inline клавиатура для вывода списка заказов +
def inline_orders_list(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    print(orders)
    text = "Ваши заказы:"
    for order_id in orders:
        builder.button(
            text=f"Заказ №{order_id} от дата",
            callback_data=OrderInfo(order_id=order_id))
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Inline клавиатура для вывода данных заказа
def inline_order_data(order_id: str, is_invoice: bool) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = f"Заказ №{order_id}"

    builder.button(text="🎫 Билеты", callback_data=f"tickets_*_{order_id}")

    if is_invoice:
        builder.button(text="Счет-договор", callback_data=f"invoice_{order_id}")
        # TODO
        builder.button(text="УПД", callback_data="1235")
        builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
        builder.adjust(1, 2, 1)
    else:
        builder.button(text="🛒 Вернутся к заказам", callback_data="orders")
        builder.adjust(1, repeat=True)

    return text, builder.as_markup()
