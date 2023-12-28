import os

import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import (inline_ticket_data, inline_ticket_types,
                                  inline_tickets_list)
from bot.utils.callbackdata import TicketInfo
from bot.utils.func_tickets import get_tickets_list
from bot.utils.func_orders import get_orders
from bot.utils.states import User

router = Router()


# Хэндлер по выбору типа билета по reply кнопке +
@router.message(User.logged_in, F.text.lower() == "билеты")
async def ticket_reply_type_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    orders = user_data.get("orders")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    if not orders:
        orders = get_orders(phone=user_data["phone"])
        await state.update_data(orders=orders)

    if orders:
        text, keyboard = inline_ticket_types(from_order=False)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет билетов")


# Хэндлер по выбору типа билета по inline кнопке (отдельно/из заказа) +
@router.callback_query(User.logged_in, F.data.startswith("ticket_types_"))
async def ticket_inline_type_view(callback: types.CallbackQuery):
    order_id = callback.data.split('_')[2]

    if order_id == "*":
        text, keyboard = inline_ticket_types(from_order=False)
    else:
        text, keyboard = inline_ticket_types(from_order=True, order_id=int(order_id))

    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по выводу билетов конкретного типа +
@router.callback_query(User.logged_in, F.data.startswith("tickets_"))
async def ticket_inline_list_view(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    orders = user_data["orders"]

    ticket_type = callback.data.split('_')[1]
    order_id = callback.data.split('_')[2]

    if order_id == "*":
        tickets_list = get_tickets_list(from_order=False, orders=orders, ticket_type=ticket_type)
        text, keyboard = inline_tickets_list(tickets_list=tickets_list, ticket_type=ticket_type, from_order=False)
    else:
        tickets_list = get_tickets_list(from_order=True, orders=orders, ticket_type=ticket_type, order_id=int(order_id))
        text, keyboard = inline_tickets_list(tickets_list=tickets_list, ticket_type=ticket_type, from_order=True,
                                             order_id=order_id)

    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по выводу данных билета +
@router.callback_query(User.logged_in, TicketInfo.filter())
async def callback_ticket_details_view(callback: types.CallbackQuery, callback_data: TicketInfo):
    order_id = callback_data.order_id
    from_order = callback_data.from_order
    ticket_id = callback_data.ticket_id
    ticket_type = callback_data.ticket_type

    text, keyboard = inline_ticket_data(order_id=order_id, from_order=from_order, ticket_id=ticket_id,
                                        ticket_type=ticket_type)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по отправке pdf билета +
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
