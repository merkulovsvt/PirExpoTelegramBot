from aiogram import F, Router, types
from aiogram.enums import ChatAction, ParseMode

from bot.callbacks.tickets_callbacks import (TicketDetails, TicketPrint,
                                             TicketsList)
from bot.data.events_data import get_event_data
from bot.data.tickets_data import (get_ticket_details, get_ticket_pdf,
                                   get_tickets_list, tickets_status_check)
from bot.keyboards.tickets_boards import (inline_ticket_details,
                                          inline_ticket_types,
                                          inline_tickets_list)
from bot.utils.config import exhibition_name
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выбору типа билета по reply кнопке
@router.message(LoggedIn(), F.text.lower().contains("билеты"))
async def ticket_type_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    tickets = await get_tickets_list(chat_id=message.chat.id, order_id="*")

    if tickets and tickets_status_check(tickets=tickets):
        if exhibition_name == "PIR":
            text, keyboard = inline_ticket_types()
        else:
            text, keyboard = inline_tickets_list(tickets=tickets, ticket_type='entry', order_id="*",
                                                 type_filtration=False)

        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет билетов")


# Хендлер по выбору типа билета по inline кнопке
@router.callback_query(LoggedIn(), F.data == "tickets_menu")
async def callback_ticket_type_view(callback: types.CallbackQuery):
    tickets = await get_tickets_list(chat_id=callback.message.chat.id, order_id="*")

    if tickets and tickets_status_check(tickets=tickets):
        if exhibition_name == "PIR":
            text, keyboard = inline_ticket_types()
        else:
            text, keyboard = inline_tickets_list(tickets=tickets, ticket_type='entry', order_id="*",
                                                 type_filtration=False)

        await callback.message.answer(text=text, reply_markup=keyboard)
    else:
        await callback.message.answer(text="К сожалению, у вас нет билетов")


# Хендлер по выводу списка билетов
@router.callback_query(LoggedIn(), TicketsList.filter())
async def callback_tickets_list_view(callback: types.CallbackQuery, callback_data: TicketsList):
    ticket_type = callback_data.ticket_type
    order_id = callback_data.order_id

    tickets = await get_tickets_list(chat_id=callback.message.chat.id, order_id=order_id)
    if exhibition_name == "PIR":
        text, keyboard = inline_tickets_list(tickets=tickets, ticket_type=ticket_type, order_id=order_id,
                                             type_filtration=True)
    else:
        text, keyboard = inline_tickets_list(tickets=tickets, ticket_type=ticket_type, order_id=order_id,
                                             type_filtration=False)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных билета +
@router.callback_query(LoggedIn(), TicketDetails.filter())
async def callback_ticket_details_view(callback: types.CallbackQuery, callback_data: TicketDetails):
    order_id = callback_data.order_id
    ticket_id = callback_data.ticket_id
    ticket_type = callback_data.ticket_type

    event_data = {}
    if ticket_type == 'event':
        ticket_details = await get_ticket_details(ticket_id=ticket_id)
        event_id = ticket_details.get('ticket_type').get("event_id")
        event_data = await get_event_data(event_id=event_id)

    text, keyboard = inline_ticket_details(event_data=event_data, order_id=order_id,
                                           ticket_id=ticket_id, ticket_type=ticket_type)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await callback.answer()


# Хендлер по отправке pdf билета по id +
@router.callback_query(LoggedIn(), TicketPrint.filter())
async def callback_ticket_print_view(callback: types.CallbackQuery, callback_data: TicketPrint):
    ticket_id = callback_data.ticket_id
    ticket_details = await get_ticket_details(ticket_id=ticket_id)

    url = ticket_details["pdf_url"]
    result = await get_ticket_pdf(url=url)
    if result:
        await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id,
                                                    action=ChatAction.UPLOAD_DOCUMENT)

        await callback.bot.send_document(callback.message.chat.id, document=types.BufferedInputFile(
            file=result, filename=f'Входной билет #{ticket_id}.pdf'), caption=f"Входной билет #{ticket_id}")
    else:
        await callback.message.answer(text=f"К сожалению, не можем прислать билет №{ticket_id}")

    await callback.answer()
