from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import exhibitors_search_menu
from bot.keyboards.reply import reply_exhibitors, reply_main
from bot.utils.func_exhibitors import load_exhibitors
from bot.utils.states import Exhibitors, User

router = Router()


# Хэндлер по меню поиска экспонентов +
@router.message(User.logged_in, F.text.lower() == "экспоненты")
async def exhibitor_menu_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    exhibitors = user_data.get("exhibitors")

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    if not exhibitors:
        exhibitors = load_exhibitors()
        await state.update_data(exhibitors=exhibitors)

    text, keyboard = exhibitors_search_menu(True)
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(F.data == "search_exhibitor")
async def callback_order_detail_view(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    text, keyboard = reply_exhibitors()
    await callback.message.answer("Введите название компании:", reply_markup=keyboard)
    await state.set_state(Exhibitors.searching)
    await callback.answer()


# Хэндлер по выходу из поиска через inline кнопку ~
@router.callback_query(F.data == "stop_search_exhibitor")
async def callback_order_detail_view(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    user_data = await state.get_data()
    text, keyboard = reply_main(phone=user_data.get("phone"))
    await state.set_state(User.logged_in)
    await callback.message.answer(text="Вы вернулись в главное меню.", reply_markup=keyboard)
    await callback.answer()


# Хэндлер по выходу из поиска через reply кнопку
@router.message(Exhibitors.searching, F.text.lower() == "отменить поиск")
async def callback_order_detail_view(message: types.Message, state: FSMContext):
    # await message.delete()

    user_data = await state.get_data()
    text, keyboard = reply_main(phone=user_data.get("phone"))
    await state.set_state(User.logged_in)
    await message.answer(text="Вы вернулись в главное меню.", reply_markup=keyboard)


# Хэндлер по поиску и выводу компаний
@router.message(Exhibitors.searching, F.text.lower() != "отменить поиск")
async def callback_order_detail_view(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    exhibitors = user_data.get("exhibitors")

    text = ""

    for exhibitor_id in exhibitors:
        if exhibitors[exhibitor_id]["name"].lower() == message.text.lower():
            location_text = ''
            for booth_id in exhibitors[exhibitor_id]["booth_data"]:
                hall_num, place_name = str(exhibitors[exhibitor_id]["booth_data"][booth_id]["hall_number"]), str(
                    exhibitors[exhibitor_id]["booth_data"][booth_id]["booth_number"])
                location_text += 'Зал ' + hall_num + ' cтенд №' + place_name
            text = "Компания " + exhibitors[exhibitor_id]["name"] + "\nОписание: " + exhibitors[exhibitor_id][
                "description"] + "\nНаходится в " + location_text
            a, keyboard = exhibitors_search_menu(False)
            await message.answer(text=text, reply_markup=keyboard, parse_mode="")
            break
    else:
        text = "Неверное название компании.\nПопробуйте снова"
        a, keyboard = reply_exhibitors()
        await message.answer(text=text, reply_markup=keyboard, parse_mode="")
    # await message.answer("Введите название компании:")
