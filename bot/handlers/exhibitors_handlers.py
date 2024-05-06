from aiogram import F, Router, types
from aiogram.enums import ChatAction, ParseMode
from aiogram.fsm.context import FSMContext

from bot.callbacks.exhibitors_callback import (ExhibitorDetails,
                                               ExhibitorsList,
                                               ExhibitorsSearchType)
from bot.data.exhibitors_data import (get_exhibitor_details,
                                      get_exhibitors_letters,
                                      get_exhibitors_list)
from bot.keyboards.exhibitors_boards import (inline_exhibitors_details,
                                             inline_exhibitors_letter_search,
                                             inline_exhibitors_list,
                                             inline_exhibitors_menu)
from bot.utils.filters import LoggedIn
from bot.utils.states import Exhibitors, User

router = Router()


# Хендлер по выводу меню экспонентов через reply кнопку
@router.message(LoggedIn(), F.text.lower().contains("экспоненты"))
async def exhibitors_menu_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    text, keyboard = inline_exhibitors_menu()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выводу меню экспонентов через inline кнопку
@router.callback_query(LoggedIn(), F.data == "exhibitors_menu")
async def callback_exhibitors_menu_view(callback: types.CallbackQuery):
    text, keyboard = inline_exhibitors_menu()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выбору варианта поиска
@router.callback_query(LoggedIn(), ExhibitorsSearchType.filter())
async def callback_exhibitors_search_type(callback: types.CallbackQuery, callback_data: ExhibitorsSearchType,
                                          state: FSMContext):
    search_type = callback_data.search_type
    new_message = callback_data.new_message

    if search_type == "letter":
        letters = await get_exhibitors_letters()
        text, keyboard = inline_exhibitors_letter_search(letters=letters["alphabet"])
        await callback.message.edit_text(text=text, reply_markup=keyboard)

    elif search_type == "name":
        await state.set_state(Exhibitors.searching)

        if new_message:
            await callback.message.answer(text="Введите название компании:")
        else:
            await callback.message.edit_text(text="Введите название компании:")

    await callback.answer()


ignore_text = ["🛒 заказы", "🎫 билеты", "🗓️ расписание", "🎉 мероприятия", "🤝 экспоненты"]


# Хендлер по поиску по названию
@router.message(Exhibitors.searching, ~F.text.lower().in_(ignore_text))
async def exhibitors_name_search(message: types.Message, state: FSMContext):
    user_input = message.text
    await state.set_state(User.logged_in)

    exhibitors = await get_exhibitors_list(full=False, letter=None, user_input=user_input)

    prev_callback_data = {"full": False, "letter": '*',
                          "user_input": user_input, "page": 1}

    text, keyboard = inline_exhibitors_list(exhibitors=list(exhibitors),
                                            prev_callback_data=prev_callback_data,
                                            list_type='name')

    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выводу списка экспонентов
@router.callback_query(LoggedIn(), ExhibitorsList.filter())
async def callback_exhibitors_search(callback: types.CallbackQuery, callback_data: ExhibitorsList):
    if callback_data.full:
        exhibitors = await get_exhibitors_list(full=True, letter=None, user_input=None)
        list_type = "full"

    elif callback_data.letter != "*":
        exhibitors = await get_exhibitors_list(full=False, letter=callback_data.letter, user_input=None)
        list_type = "letter"

    else:
        exhibitors = await get_exhibitors_list(full=False, letter=None, user_input=callback_data.user_input)
        list_type = "name"

    prev_callback_data = {"full": callback_data.full, "letter": callback_data.letter,
                          "user_input": callback_data.user_input, "page": callback_data.page}

    text, keyboard = inline_exhibitors_list(exhibitors=list(exhibitors),
                                            prev_callback_data=prev_callback_data,
                                            list_type=list_type)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер для вывода данных экспонента
@router.callback_query(LoggedIn(), ExhibitorDetails.filter())
async def callback_exhibitor_details(callback: types.CallbackQuery, callback_data: ExhibitorDetails):
    exhibitor_id = callback_data.exhibitor_id

    exhibitor_details = await get_exhibitor_details(exhibitor_id=exhibitor_id)

    exhibitors_list_data = {"full": callback_data.full, "letter": callback_data.letter,
                            "page": callback_data.page, "user_input": callback_data.user_input}

    text, keyboard = inline_exhibitors_details(exhibitor_details=exhibitor_details,
                                               exhibitors_list_data=exhibitors_list_data)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await callback.answer()


# Хендлер для inactive кнопок
@router.callback_query(F.data == "inactive")
async def callback_inactive(callback: types.CallbackQuery):
    await callback.answer()
