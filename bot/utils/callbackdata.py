from aiogram.filters.callback_data import CallbackData


class OrderInfo(CallbackData, prefix="order"):
    order_id: int


class TicketInfo(CallbackData, prefix="ticket"):
    order_id: int
    from_order: bool
    ticket_id: int
    ticket_type: str
