from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.orders_callbacks import InvoicePrint, OrderDetails
from bot.callbacks.tickets_callbacks import TicketsList
from bot.data.orders_data import tickets_status_check


# Inline клавиатура для вывода списка заказов
def inline_orders_list(orders: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()

    orders_list = []
    for order in orders:
        if order["status"] == 3 and tickets_status_check(order=order):
            date = datetime.fromisoformat(order['date']).strftime('%d.%m.%Y')
            orders_list.append((date, order["id"]))

    if orders_list:
        text = "Ваши заказы:"

        for order in sorted(orders_list, key=lambda x: x[0]):
            button_text = f"Заказ №{order[1]} от {order[0]}"

            order_id = str(order[1])
            builder.button(text=button_text, callback_data=OrderDetails(order_id=order_id))
    else:
        text = "К сожалению, у вас нет заказов"

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода деталей заказа
def inline_order_details(order_id: str, order_details: dict) -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    date = datetime.fromisoformat(order_details['date']).strftime('%d.%m.%Y')

    text = (f"Детали заказа №{order_id}:\n"
            f"Дата заказа {date}.\n"
            f"Сумма заказа: {order_details.get('sum')} руб.")

    if order_details["status"] == 3:
        builder.button(text="🎫 Билеты", callback_data=TicketsList(ticket_type="*", order_id=order_id))
        builder.button(text="Возврат", url=order_details["return_request_url"])

        if order_details.get("invoice_pdf_url"):
            builder.button(text="Счет-договор", callback_data=InvoicePrint(order_id=order_id))
            builder.button(text="УПД", callback_data="1235")  # Доделать
            builder.button(text="🛒 Вернутся к заказам", callback_data="orders_list")

            builder.adjust(2, 2, 1)
        else:
            builder.button(text="🛒 Вернутся к заказам", callback_data="orders_list")

            builder.adjust(2, 1)

    return text, builder.as_markup()
