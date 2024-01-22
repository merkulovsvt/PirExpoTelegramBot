from aiogram.filters.callback_data import CallbackData


class OrderInfo(CallbackData, prefix="order"):
    order_id: str


class TicketInfo(CallbackData, prefix="ticket"):
    order_id: str
    ticket_id: str
    ticket_type: str


class EventInfo(CallbackData, prefix="event"):
    event_id: str
    theme_id: str
    ticket_type: str


class ExhibitorSearchInfo(CallbackData, prefix="exhibitor_search"):
    full: bool
    letter: str
    page: int
    user_input: str


class ExhibitorInfo(CallbackData, prefix="exhibitor"):
    exhibitor_id: int
    full: bool
    letter: str
    page: int
    user_input: str
