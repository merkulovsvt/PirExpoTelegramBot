import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction, ParseMode

from bot.data.events_data import get_event_data
from bot.data.tickets_data import (get_ticket_details, get_tickets_list,
                                   tickets_status_check)
from bot.keyboards.tickets_boards import (inline_ticket_details,
                                          inline_ticket_types,
                                          inline_tickets_list)
from bot.utils.callbackdata import TicketInfo
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выбору типа билета по reply кнопки +
@router.message(LoggedIn(), F.text.lower() == "🎫 билеты")
async def ticket_type_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    tickets = get_tickets_list(chat_id=message.chat.id, order_id="*")

    if tickets and tickets_status_check(tickets=tickets):
        text, keyboard = inline_ticket_types()
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет билетов")


# Хендлер по выбору типа билета по inline кнопки +
@router.callback_query(LoggedIn(), F.data == "ticket_types")
async def callback_ticket_type_view(callback: types.CallbackQuery):
    tickets = get_tickets_list(chat_id=callback.message.chat.id, order_id="*")

    if tickets and tickets_status_check(tickets=tickets):
        text, keyboard = inline_ticket_types()
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text="К сожалению, у вас нет билетов")

    await callback.answer()


# Хендлер по выводу списка билетов +
@router.callback_query(LoggedIn(), F.data.startswith("tickets_"))
async def callback_ticket_list_view(callback: types.CallbackQuery):
    ticket_type = callback.data.split("_")[1]
    order_id = callback.data.split("_")[2]
    tickets = get_tickets_list(chat_id=callback.message.chat.id, order_id=order_id)

    text, keyboard = inline_tickets_list(tickets=tickets, ticket_type=ticket_type, order_id=order_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных билета +
@router.callback_query(LoggedIn(), TicketInfo.filter())
async def callback_ticket_details_view(callback: types.CallbackQuery, callback_data: TicketInfo):
    order_id = callback_data.order_id
    ticket_id = callback_data.ticket_id
    ticket_type = callback_data.ticket_type

    event_data = {}
    if ticket_type == 'event':
        event_id = get_ticket_details(ticket_id=ticket_id).get('ticket_type').get("event_id")
        event_data = get_event_data(event_id=event_id)

    text, keyboard = inline_ticket_details(event_data=event_data, order_id=order_id,
                                           ticket_id=ticket_id, ticket_type=ticket_type)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await callback.answer()


# Хендлер по отправке pdf билета по id +
@router.callback_query(LoggedIn(), F.data.startswith("ticket_print_"))
async def callback_ticket_print_view(callback: types.CallbackQuery):
    ticket_id = callback.data.split('_')[2]
    url = get_ticket_details(ticket_id=ticket_id)["pdf_url"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.read()
                await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id,
                                                            action=ChatAction.UPLOAD_DOCUMENT)

                await callback.bot.send_document(callback.message.chat.id, document=types.BufferedInputFile(
                    file=result, filename=f'Входной билет #{ticket_id}.pdf'), caption=f"Входной билет #{ticket_id}")
            else:
                await callback.message.answer(text=f"К сожалению, не можем прислать билет №{ticket_id}")

    await callback.answer()
