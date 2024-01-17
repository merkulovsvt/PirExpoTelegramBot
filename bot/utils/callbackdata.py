from aiogram.filters.callback_data import CallbackData


class OrderInfo(CallbackData, prefix="order"):
    order_id: str


class TicketInfo(CallbackData, prefix="ticket"):
    order_id: str
    ticket_id: str
    ticket_type: str
