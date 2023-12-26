import os
from http import HTTPStatus
from aiogram.enums import ChatAction

import requests
from aiogram import F, Router, types
import aiohttp
from aiogram.fsm.context import FSMContext
from requests.auth import HTTPBasicAuth

from bot.keyboards.inline import (inline_order_data,
                                  inline_orders, inline_start,
                                  inline_ticket_data, inline_tickets)
from bot.keyboards.reply import reply_main
from bot.utils.callbackdata import OrderInfo, TicketInfo
from bot.utils.config import User, orders_get

router = Router()


# Хэндлер по выводу списка всех билетов по reply кнопке
@router.message(User.logged_in, F.text.lower() == "билеты")
async def tickets_list_view(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    orders = orders_get(user_data["phone"])
    if not user_data.get("orders"):
        await state.update_data(orders=orders)

    order_ids, ticket_ids = [], []
    for order_id in orders:
        for ticket_id in orders[order_id]['ticket_ids']:
            order_ids.append(order_id)
            ticket_ids.append(ticket_id)

    text, keyboard = inline_tickets(order_ids, ticket_ids)

    await callback.answer(text=text, reply_markup=keyboard)


# Хэндлер по выводу списка билетов по inline кнопке (из заказа/отдельно)
@router.callback_query(User.logged_in, F.data.startswith("tickets_"))
async def callback_order_tickets_list_view(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.data.split('_')[1]
    user_data = await state.get_data()
    if order_id == '*':

        order_ids, ticket_ids = [], []
        for order_id in user_data["orders"]:
            for ticket_id in user_data["orders"][order_id]['ticket_ids']:
                order_ids.append(order_id)
                ticket_ids.append(ticket_id)

        text, keyboard = inline_tickets(order_ids, ticket_ids)
    else:
        text, keyboard = inline_tickets(int(order_id), user_data["orders"][int(order_id)]['ticket_ids'])

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по выводу данных билета
@router.callback_query(User.logged_in, TicketInfo.filter())
async def callback_ticket_details_view(callback: types.CallbackQuery, callback_data: TicketInfo):
    text, keyboard = inline_ticket_data(callback_data.order_id, callback_data.ticket_id, callback_data.from_order)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


from bot.utils.config import url_ticket_print


# Хэндлер по отправке билета
@router.callback_query(User.logged_in, F.data.startswith("print_ticket_"))
async def callback_ticket_print_view(callback: types.CallbackQuery, state: FSMContext):
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
                                                                                  filename=f'Билет #{ticket_id}.pdf'))
            else:
                await callback.message.answer(text=f"К сожалению, не можем прислать билет №{ticket_id}")

            await callback.answer()
