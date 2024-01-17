from aiogram import F, Router, types
from aiogram.enums import ChatAction

from bot.data.tickets_data import get_tickets_list, get_ticket_data
from bot.keyboards.tickets_boards import (inline_ticket_types,
                                          inline_tickets_list, inline_ticket_data)
from bot.utils.callbackdata import TicketInfo
from bot.utils.states import User

router = Router()


# Хендлер по выбору типа билета из reply кнопки +
@router.message(User.logged_in, F.text.lower() == "🎫 билеты")
async def ticket_type_view(message: types.Message):
    tickets = get_tickets_list(chat_id=message.chat.id)
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    if tickets:
        text, keyboard = inline_ticket_types()
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет билетов")


# Хендлер по выбору типа билета из inline кнопки +
@router.callback_query(User.logged_in, F.data.startswith("ticket_types"))
async def callback_ticket_type_view(callback: types.CallbackQuery):
    tickets = get_tickets_list(chat_id=callback.message.chat.id)

    if tickets:
        text, keyboard = inline_ticket_types()
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text="К сожалению, у вас нет билетов")

    await callback.answer()


# Хендлер по выводу списка билетов по reply и из заказов +
@router.callback_query(User.logged_in, F.data.startswith("tickets_"))
async def callback_ticket_list_view(callback: types.CallbackQuery):
    tickets = get_tickets_list(chat_id=callback.message.chat.id)
    ticket_type = callback.data.split("_")[1]
    order_id = callback.data.split("_")[2]

    text, keyboard = inline_tickets_list(tickets=tickets, ticket_type=ticket_type, order_id=order_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных билета +
@router.callback_query(User.logged_in, TicketInfo.filter())
async def callback_ticket_details_view(callback: types.CallbackQuery, callback_data: TicketInfo):
    order_id = callback_data.order_id
    ticket_id = callback_data.ticket_id
    ticket_type = callback_data.ticket_type

    ticket_data = get_ticket_data(ticket_id=ticket_id)
    text, keyboard = inline_ticket_data(ticket_data=ticket_data, order_id=order_id,
                                        ticket_id=ticket_id, ticket_type=ticket_type)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

# Хендлер по отправке pdf билета +
@router.callback_query(User.logged_in, F.data.startswith("print_ticket_"))
async def callback_ticket_print_view(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split('_')[2])
    url = f"https://master.apiv2.pir.ru/api/v1/ticket/{ticket_id}/print?pdf"

    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=aiohttp.BasicAuth(login, password)) as response:
            if response.status == 200:
                result = await response.read()
                await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id,
                                                            action=ChatAction.UPLOAD_DOCUMENT)

                await callback.bot.send_document(callback.message.chat.id,
                                                 document=types.BufferedInputFile(file=result,
                                                                                  filename=f'Билет #{ticket_id}.pdf'),
                                                 caption=f"Входной билет #{ticket_id}")
            else:
                await callback.message.answer(text=f"К сожалению, не можем прислать билет №{ticket_id}")

    await callback.answer()
