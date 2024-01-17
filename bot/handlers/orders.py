from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot.keyboards.orders_boards import inline_order_data, inline_orders_list
from bot.utils.callbackdata import OrderInfo
from bot.data.func_orders import get_orders
from bot.utils.states import User

router = Router()


# Хендлер по выводу списка заказов по reply кнопке +
@router.message(User.logged_in, F.text.lower() == "🛒 заказы")
async def orders_list_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    orders = user_data.get("orders")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    if not orders:
        orders = get_orders(phone=user_data["phone"])
        await state.update_data(orders=orders)

    if orders:
        text, keyboard = inline_orders_list(orders=orders)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="К сожалению, у вас нет заказов")


# Хендлер по выводу списка заказов по inline кнопке
@router.callback_query(User.logged_in, F.data == "orders")
async def callback_order_detail_view(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    orders = user_data.get("orders")

    text, keyboard = inline_orders_list(orders)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных заказа
@router.callback_query(User.logged_in, OrderInfo.filter())
async def callback_order_details_view(callback: types.CallbackQuery, callback_data: OrderInfo, state: FSMContext):
    user_data = await state.get_data()
    if user_data["orders"][str(callback_data.order_id)]["invoice_url"] is not None:
        is_invoice = True
    else:
        is_invoice = False

    text, keyboard = inline_order_data(order_id=callback_data.order_id, is_invoice=is_invoice)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по отправке счета заказа
@router.callback_query(User.logged_in, F.data.startswith("invoice_"))
async def callback_order_invoice_view(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[1])
    user_data = await state.get_data()
    pdf_url = user_data["orders"][order_id]["invoice_url"]

    if pdf_url:
        await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
        await callback.message.reply_document(document=types.URLInputFile(pdf_url, filename=f"invoice_{order_id}.pdf "),
                                              caption=f"Счет-договор по заказу #{order_id}")
    else:
        await callback.message.answer(text=f"К сожалению, не можем прислать счет-договор к заказу №{order_id}")
    await callback.answer()
