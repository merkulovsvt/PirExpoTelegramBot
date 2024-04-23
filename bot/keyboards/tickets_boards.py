from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.events_callbacks import EventPrint
from bot.callbacks.orders_callbacks import OrderDetails
from bot.callbacks.tickets_callbacks import (TicketDetails, TicketPrint,
                                             TicketsList)


# Inline клавиатура для выбора типа билета +
def inline_ticket_types() -> (str, InlineKeyboardMarkup):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип билета"

    builder.button(text="Входные билеты", callback_data=TicketsList(ticket_type="entry", order_id="*"))
    builder.button(text="Мероприятия", callback_data=TicketsList(ticket_type="event", order_id="*"))
    builder.adjust(2)

    return text, builder.as_markup()


# Inline клавиатура для вывода списка билетов (для orders, в том числе)
def inline_tickets_list(tickets: dict, ticket_type: str, order_id: str):
    builder = InlineKeyboardBuilder()
    list_empty = True

    if ticket_type == "entry":
        text = "Входные билеты:"
        return_button_text = "🎫 Вернуться к выбору категории"
        callback_data = "tickets_menu"

    elif ticket_type == "event":
        text = "Билеты на мероприятия:"
        return_button_text = "🎫 Вернуться к выбору категории"
        callback_data = "tickets_menu"

    else:
        text = f"Билеты заказа №{order_id}"
        return_button_text = "🛒 Вернуться к заказу"
        callback_data = OrderDetails(order_id=order_id)

    tickets_set = set()
    for ticket in tickets:
        tickets_set.add((ticket['id'], ticket["ticket_type"]["is_event"],
                         ticket['ticket_type']['name'], ticket['status']))

    for ticket in sorted(tickets_set, key=lambda x: (x[1], len(x[2]))):
        if ticket[1]:
            event_name = ticket[2].strip("\"")
            button_text = f"Билет №{ticket[0]} \"{event_name}\""
        else:
            button_text = f"Входной билет №{ticket[0]}"
            # button_text = f"Входной билет №{ticket['id']} на {tickets[ticket_id]['ticket_owner_name']}" #TODO

        if (ticket_type == "*" or (ticket[1] and ticket_type == "event") or (
                not ticket[1] and ticket_type == "entry")) and ticket[3] == "2":
            list_empty = False
            builder.button(text=button_text, callback_data=TicketDetails(order_id=order_id,
                                                                         ticket_id=str(ticket[0]),
                                                                         ticket_type="event" if ticket[1] else "entry"))

    if ticket_type != "*" and list_empty:
        text = "К сожалению, у вас нет билетов в данной категории"
    elif ticket_type == "*" and list_empty:
        text = "К сожалению, у вас нет билетов в данном заказе"

    builder.button(text=return_button_text, callback_data=callback_data)
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


# Inline клавиатура для вывода деталей билета
def inline_ticket_details(event_data: dict, order_id: str, ticket_id: str, ticket_type: str):
    builder = InlineKeyboardBuilder()
    if ticket_type == "entry":
        builder.button(text="Скачать", callback_data=TicketPrint(ticket_id=ticket_id))

        # text = f"Входной билет №{ticket_id} на {ticket_details['ticket_owner_name']}" #TODO
        text = f"Входной билет №{ticket_id}\n"
        # + f"Принадлежит заказу №{order_id}.")
        builder.button(text="Редактировать", url="zaza.com")  # Ждём ссылку от Леши

        if order_id != "*":
            ticket_type = "*"

        builder.button(text="🎫 Вернуться к списку билетов",
                       callback_data=TicketsList(ticket_type=ticket_type, order_id=order_id))
        builder.adjust(2, 1, 1)

    else:
        name = event_data.get('name').strip("\"")
        type_name = event_data.get('type').get('name')
        ticket_type_id = event_data.get('ticket_type').get('id')

        date = datetime.fromisoformat(event_data.get("time_start")).strftime('%d.%m.%Y')
        time_start = datetime.fromisoformat(event_data.get("time_start")).strftime('%H:%M')
        time_finish = datetime.fromisoformat(event_data.get('time_finish')).strftime('%H:%M')

        text = (f"<b>Дата:</b> <i>{date}</i>\n\n"
                f"<b>Время:</b> <i>{time_start}</i> - <i>{time_finish}</i>\n\n"
                f"<b>{type_name}</b>: \"{name}\"\n\n"
                f"<b>Место</b>: {event_data['place'].get('name') if event_data.get('place') else ''}")

        builder.button(text="Скачать билет", callback_data=EventPrint(ticket_type_id=str(ticket_type_id)))
        builder.adjust(1, 1)

        if order_id != "*":
            ticket_type = "*"

        builder.button(text="🎫 Вернуться к списку билетов",
                       callback_data=TicketsList(ticket_type=ticket_type, order_id=order_id))
        builder.adjust(1, repeat=True)

    return text, builder.as_markup()
