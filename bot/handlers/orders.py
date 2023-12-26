import os

import requests
from aiogram import F, Router, types, methods
from aiogram.fsm.context import FSMContext
from requests.auth import HTTPBasicAuth
from aiogram.types import URLInputFile
from aiogram.enums import ChatAction

from bot.keyboards.inline import (inline_order_data,
                                  inline_orders, inline_start,
                                  inline_ticket_data, inline_tickets)
from bot.keyboards.reply import reply_main
from bot.utils.callbackdata import OrderInfo, TicketInfo
from bot.utils.config import User, orders_get

router = Router()


# Хэндлер по выводу списка заказов по reply кнопке
@router.message(User.logged_in, F.text.lower() == "заказы")
async def orders_list_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    orders = orders_get(user_data['phone'])
    if not user_data.get("orders"):
        await state.update_data(orders=orders)

    text, keyboard = inline_orders(orders)
    await message.answer(text, reply_markup=keyboard)


# Хэндлер по выводу списка заказов по inline кнопке
@router.callback_query(User.logged_in, F.data == "orders")
async def callback_order_detail_view(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    orders = orders_get(user_data['phone'])

    text, keyboard = inline_orders(orders)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по выводу данных заказа
@router.callback_query(User.logged_in, OrderInfo.filter())
async def callback_order_details_view(callback: types.CallbackQuery, callback_data: OrderInfo):
    text, keyboard = inline_order_data(callback_data.order_id)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Хэндлер по отправке счета заказа
@router.callback_query(User.logged_in, F.data.startswith("invoice_"))
async def callback_order_invoice_view(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split('_')[1])
    user_data = await state.get_data()
    pdf_url = user_data["orders"][order_id]['invoice_url']

    if pdf_url:
        # Как поменять название файла при отправке
        await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
        await callback.bot.send_document(callback.message.chat.id, document=pdf_url,
                                         caption=f"Счет договор по заказу #{order_id}")

        # await callback.message.reply_document(document=types.URLInputFile(pdf_url, filename=f"invoice_{order_id}.pdf "))
    else:
        await callback.message.answer(text=f"К сожалению, не можем прислать счет-договор к заказу №{order_id}")
    await callback.answer()
