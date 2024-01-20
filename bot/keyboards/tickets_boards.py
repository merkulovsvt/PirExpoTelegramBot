from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import OrderInfo, TicketInfo


# Inline клавиатура для выбора типа билета +
def inline_ticket_types() -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип билета"

    builder.button(text="Входные билеты", callback_data="tickets_entry_*")
    builder.button(text="Мероприятия", callback_data="tickets_event_*")
    builder.adjust(2)

    return text, builder.as_markup()


# Inline клавиатура для вывода списка билетов
def inline_tickets_list(tickets: dict, ticket_type: str, order_id: str):
    builder = InlineKeyboardBuilder()
    list_empty = True

    if ticket_type == "entry":
        text = "Входные билеты:"
        return_button_text = "Вернуться к выбору категории"
        callback_data = "ticket_types"

    elif ticket_type == "event":
        text = "Билеты на мероприятия:"
        return_button_text = "Вернуться к выбору категории"
        callback_data = "ticket_types"

    else:
        text = f"Билеты заказа №{order_id}"
        return_button_text = "Вернуться к заказу"
        callback_data = OrderInfo(order_id=order_id)

    for ticket in tickets:
        if ticket["ticket_type"]["is_event"]:
            button_text = f"Билет №{ticket['id']} на мероприятие {ticket['ticket_type']['name']}"
        else:
            button_text = f"Входной билет №{ticket['id']}"
            # button_text = f"Входной билет №{ticket['id']} на {tickets[ticket_id]['ticket_owner_name']}"

        if (ticket_type == "*" or (ticket["ticket_type"]["is_event"] and ticket_type == "event") or (
                not ticket["ticket_type"]["is_event"] and ticket_type == "entry")) and ticket["status"] == "2":
            list_empty = False
            builder.button(text=button_text,
                           callback_data=TicketInfo(order_id=order_id, ticket_id=str(ticket["id"]),
                                                    ticket_type="event" if ticket["ticket_type"]["is_event"]
                                                    else "entry"))

    if ticket_type != "*" and list_empty:
        text = "К сожалению, у вас нет билетов в данной категории"
    elif ticket_type == "*" and list_empty:
        text = "К сожалению, у вас нет билетов в данном заказе"

    builder.button(text=return_button_text, callback_data=callback_data)
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Inline клавиатура для вывода деталей билета ~
def inline_ticket_details(ticket_details: dict, order_id: str, ticket_id: str, ticket_type: str):
    builder = InlineKeyboardBuilder()

    builder.button(text="Скачать", callback_data=f"ticket_print_{ticket_id}")

    if ticket_type == "entry":
        # text = f"Входной билет №{ticket_id} на {ticket_details['ticket_owner_name']}"
        text = f"Входной билет №{ticket_id}"
        builder.button(text="Редактировать", url="zaza.com")  # Ждём ссылку от Леши

    # elif ticket_type == "event":
    else:
        text = f"Билет №{ticket_id} на мероприятие {ticket_details['event_name']}"
        builder.button(text="Информация о мероприятии", callback_data="event")  # Доделать

    if order_id != "*":
        ticket_type = "*"

    builder.button(text="🎫 Вернуться к списку билетов", callback_data=f"tickets_{ticket_type}_{order_id}")
    builder.adjust(2, 1, 1)

    return text, builder.as_markup()
