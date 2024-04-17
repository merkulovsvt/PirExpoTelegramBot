from aiogram.filters.callback_data import CallbackData


class OrderDetails(CallbackData, prefix="order_details"):
    order_id: str


class InvoicePrint(CallbackData, prefix="invoice_print"):
    order_id: str
