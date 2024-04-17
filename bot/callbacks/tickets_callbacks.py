from aiogram.filters.callback_data import CallbackData


class TicketsList(CallbackData, prefix="tickets_list"):
    ticket_type: str
    order_id: str


class TicketDetails(CallbackData, prefix="ticket_details"):
    order_id: str
    ticket_id: str
    ticket_type: str


class TicketPrint(CallbackData, prefix="ticket_print"):
    ticket_id: str
