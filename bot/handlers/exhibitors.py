from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.data.exhibitors_data import (get_exhibitor_details,
                                      get_exhibitors_letters,
                                      get_exhibitors_list)
from bot.keyboards.exhibitors_boards import (inline_exhibitors_details,
                                             inline_exhibitors_letter_search,
                                             inline_exhibitors_list,
                                             inline_exhibitors_list_by_name,
                                             inline_exhibitors_menu)
from bot.utils.callbackdata import ExhibitorInfo, ExhibitorSearchInfo
from bot.utils.filters import LoggedIn
from bot.utils.states import Exhibitors, User

router = Router()


# Хендлер по выводу меню экспонентов через reply кнопку +
@router.message(LoggedIn(), F.text.lower() == "🤝 экспоненты")
async def exhibitors_menu_view(message: types.Message):
    text, keyboard = inline_exhibitors_menu()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выводу меню экспонентов через inline кнопку +
@router.callback_query(LoggedIn(), F.data == "exhibitors_menu")
async def callback_exhibitors_menu_view(callback: types.CallbackQuery):
    text, keyboard = inline_exhibitors_menu()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу меню поиска по типу +
@router.callback_query(LoggedIn(), F.data.startswith("exhibitors_searching_"))
async def callback_exhibitors_search_type(callback: types.CallbackQuery, state: FSMContext):
    search_type = callback.data.split("_")[2]

    if search_type == "letter":
        letters = get_exhibitors_letters()
        text, keyboard = inline_exhibitors_letter_search(letters=letters["alphabet"])
        await callback.message.edit_text(text=text, reply_markup=keyboard)

    elif search_type == "name":
        await state.set_state(Exhibitors.searching)
        await callback.message.answer(text="Введите название компании:")

    await callback.answer()


ignore_text = ["🛒 Заказы", "🎫 Билеты", "🗓️ Расписание", "🎉 Мероприятия", "🤝 Экспоненты"]


# Хендлер по поиску по названию +
@router.message(Exhibitors.searching, ~F.text.lower().in_(ignore_text))
async def exhibitors_name_search(message: types.Message, state: FSMContext):
    user_input = message.text
    exhibitors = get_exhibitors_list(user_input=user_input)
    await state.set_state(User.logged_in)

    text, keyboard = inline_exhibitors_list_by_name(exhibitors=exhibitors, page=1, user_input=user_input)
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по поиску через inline кнопку +
@router.callback_query(LoggedIn(), ExhibitorSearchInfo.filter())
async def callback_exhibitors_search(callback: types.CallbackQuery, callback_data: ExhibitorSearchInfo):
    if callback_data.full:
        exhibitors = get_exhibitors_list(full=True)
        list_type = "full"
    elif callback_data.letter != "*":
        exhibitors = get_exhibitors_list(letter=callback_data.letter)
        list_type = "letter"
    else:
        exhibitors = get_exhibitors_list(user_input=callback_data.user_input)
        list_type = "name"

    prev_callback_data = {"full": callback_data.full, "letter": callback_data.letter,
                          "user_input": callback_data.user_input, "page": callback_data.page}

    text, keyboard = inline_exhibitors_list(exhibitors=exhibitors,
                                            prev_callback_data=prev_callback_data,
                                            list_type=list_type)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер для вывода данных экспонента +
@router.callback_query(LoggedIn(), ExhibitorInfo.filter())
async def callback_exhibitor_details(callback: types.CallbackQuery, callback_data: ExhibitorInfo):
    exhibitor_id = callback_data.exhibitor_id
    exhibitor_details = get_exhibitor_details(exhibitor_id=exhibitor_id)

    exhibitors_list_data = {"full": callback_data.full, "letter": callback_data.letter,
                            "page": callback_data.page, "user_input": callback_data.user_input}
    text, keyboard = inline_exhibitors_details(exhibitor_details=exhibitor_details,
                                               exhibitors_list_data=exhibitors_list_data)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


# Хендлер для inactive кнопок +
@router.callback_query(F.data == "inactive")
async def callback_inactive(callback: types.CallbackQuery):
    await callback.answer()
