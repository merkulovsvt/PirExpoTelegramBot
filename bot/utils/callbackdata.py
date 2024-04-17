from aiogram.filters.callback_data import CallbackData


class OrderInfo(CallbackData, prefix="get_order_info"):
    order_id: str


class TicketInfo(CallbackData, prefix="ticket"):
    order_id: str
    ticket_id: str
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


class PartnerTypes(CallbackData, prefix="get_partner_types_list"):
    theme_id: int


class PartnersList(CallbackData, prefix="get_partners_list"):
    theme_id: str
    type_id: str
