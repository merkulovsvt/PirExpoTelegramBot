import os

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import requests
from requests.auth import HTTPBasicAuth

from bot.keyboards.inline import inline_start, inline_orders, inline_order, inline_tickets, inline_ticket
from bot.keyboards.reply import reply_main
from bot.data import User
from bot.keyboards.inline import OrderInfo, TicketInfo

router = Router()


@router.message(User.logged_in, F.text.lower() == "заказы")
async def command_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    payload = {"phone": user_data["phone"]}
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password), params=payload)
    orders = {}
    for order in r.json():
        for order_item in order["order_items"]:
            if order["id"] not in orders:
                orders[order["id"]] = []
            orders[order["id"]].append(order_item["id"])
    await state.update_data(orders=orders)

    await message.answer(inline_orders(orders)[0], reply_markup=inline_orders(orders)[1])


# ебанутый костыль (как соединить эти две функции в одну?)
@router.callback_query(User.logged_in, F.data == "orders")
async def callback_orders_view(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(inline_orders(user_data["orders"])[0],
                                     reply_markup=inline_orders(user_data["orders"])[1])
    await callback.answer()


@router.callback_query(User.logged_in, OrderInfo.filter())
async def callback_order_view(callback: types.CallbackQuery, callback_data: OrderInfo):
    await callback.message.edit_text(inline_order(callback_data.order_id)[0],
                                     reply_markup=inline_order(callback_data.order_id)[1])
    await callback.answer()


@router.callback_query(User.logged_in, F.data.startswith("tickets_"))
async def callback_order_view(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split('_')[1])
    user_data = await state.get_data()
    await callback.message.edit_text(inline_tickets(user_data["orders"][order_id], order_id)[0],
                                     reply_markup=inline_tickets(user_data["orders"][order_id], order_id)[1])
    await callback.answer()


@router.callback_query(User.logged_in, TicketInfo.filter())
async def callback_order_view(callback: types.CallbackQuery, callback_data: TicketInfo):
    await callback.message.edit_text(inline_ticket(callback_data.order_id, callback_data.ticket_id)[0],
                                     reply_markup=inline_ticket(callback_data.order_id, callback_data.ticket_id)[1])
    await callback.answer()
