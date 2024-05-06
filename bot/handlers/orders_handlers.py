import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction

from bot.callbacks.orders_callbacks import InvoicePrint, OrderDetails
from bot.data.orders_data import get_order_details, get_orders_list
from bot.keyboards.orders_boards import (inline_order_details,
                                         inline_orders_list)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выводу списка заказов по reply кнопке
@router.message(LoggedIn(), F.text.lower().contains("заказы"))
async def orders_list_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    orders = await get_orders_list(chat_id=message.chat.id)

    if orders:
        text, keyboard = inline_orders_list(orders=orders)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет заказов")


# Хендлер по выводу списка заказов по inline кнопке
@router.callback_query(LoggedIn(), F.data == "orders_list")
async def callback_orders_list_view(callback: types.CallbackQuery):
    orders = await get_orders_list(chat_id=callback.message.chat.id)

    if orders:
        text, keyboard = inline_orders_list(orders=orders)
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text="К сожалению, у вас нет заказов")
    await callback.answer()


# Хендлер по выводу деталей заказа
@router.callback_query(LoggedIn(), OrderDetails.filter())
async def callback_order_details_view(callback: types.CallbackQuery, callback_data: OrderDetails):
    order_id = callback_data.order_id

    order_details = await get_order_details(order_id=order_id)

    text, keyboard = inline_order_details(order_id=order_id, order_details=order_details)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по отправке счета заказа
@router.callback_query(LoggedIn(), InvoicePrint.filter())
async def callback_order_invoice_send(callback: types.CallbackQuery, callback_data: InvoicePrint):
    order_id = callback_data.order_id

    order_details = await get_order_details(order_id=order_id)
    url = order_details["invoice_pdf_url"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.read()
                await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id,
                                                            action=ChatAction.UPLOAD_DOCUMENT)

                await callback.bot.send_document(callback.message.chat.id, document=types.BufferedInputFile(
                    file=result, filename=f'invoice_{order_id}.pdf'), caption=f"Счет-договор по заказу #{order_id}")
            else:
                await callback.message.answer(text=f"К сожалению, не можем прислать счет-договор к заказу №{order_id}")
    await callback.answer()
