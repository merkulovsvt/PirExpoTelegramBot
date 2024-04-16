import math

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbackdata import ExhibitorInfo, ExhibitorSearchInfo


# Inline клавиатура для меню экспонентов +
def inline_exhibitors_menu():
    builder = InlineKeyboardBuilder()
    text = "Это меню экспонентов. Нажмите на кнопку для продолжения."

    builder.button(text="Поиск по названию", callback_data="exhibitors_searching_name")
    builder.button(text="Поиск по алфавиту", callback_data="exhibitors_searching_letter")

    builder.button(text="Все экспоненты",
                   callback_data=ExhibitorSearchInfo(full=True, letter="*", page=1, user_input="*"))
    builder.adjust(2, 1)
    return text, builder.as_markup()


# Inline клавиатура для поиска по букве
def inline_exhibitors_letter_search(letters: list):
    builder = InlineKeyboardBuilder()
    text = "Выберите первый символ поиска:"

    for letter in letters:
        builder.button(text=letter,
                       callback_data=ExhibitorSearchInfo(full=False, letter=letter, page=1, user_input="*"))
    builder.adjust(5, repeat=True)

    builder.row(InlineKeyboardButton(text="Отменить поиск", callback_data="exhibitors_menu"))

    return text, builder.as_markup()

# Inline клавиатура для вывода списка экспонентов по названию (старт)
def inline_exhibitors_list_by_name(exhibitors: list, page: int, user_input: str):
    builder = InlineKeyboardBuilder()

    if exhibitors:
        text = "Экспоненты:"
        buttons_on_page = 7
        exhibitors_set = set()

        for exhibitor in exhibitors:
            exhibitors_set.add((exhibitor["name"], exhibitor["id"]))

        pages_count = math.ceil(len(exhibitors_set) / buttons_on_page)

        if page <= 0:
            page = 1
        elif page > pages_count:
            page = pages_count

        buttons_count = 0
        for exhibitor in sorted(exhibitors_set)[(page - 1) * buttons_on_page:page * buttons_on_page]:
            buttons_count += 1
            builder.button(text=exhibitor[0],
                           callback_data=ExhibitorInfo(exhibitor_id=exhibitor[1], full=False, letter="*", page=page,
                                                       user_input=user_input))

        builder.adjust(1)

        if len(exhibitors) > buttons_on_page:
            builder.button(text="←", callback_data=ExhibitorSearchInfo(full=False, letter="*", page=page - 1,
                                                                       user_input=user_input) if page > 1 else "inactive")
            builder.button(text=f"{page}/{pages_count}", callback_data="inactive")
            builder.button(text="→", callback_data=ExhibitorSearchInfo(full=False, letter="*", page=page + 1,
                                                                       user_input=user_input) if page < pages_count else "inactive")
            builder.adjust(*[1 for _ in range(buttons_count)], 3)

    else:
        text = "По вашему запросу компаний не найдено"

    builder.row(InlineKeyboardButton(text="Продолжить поиск", callback_data=f"exhibitors_searching_name"),
                InlineKeyboardButton(text="Отменить поиск", callback_data="exhibitors_menu"))

    return text, builder.as_markup()


# Inline клавиатура для вывода списка экспонентов
def inline_exhibitors_list(exhibitors: list, prev_callback_data: dict, list_type: str):
    builder = InlineKeyboardBuilder()

    full = prev_callback_data["full"]
    letter = prev_callback_data["letter"]
    page = prev_callback_data["page"]
    user_input = prev_callback_data["user_input"]

    if exhibitors:
        text = "Экспоненты:"
        buttons_on_page = 7
        exhibitors_set = set()

        for exhibitor in exhibitors:
            exhibitors_set.add((exhibitor["name"], exhibitor["id"]))

        pages_count = math.ceil(len(exhibitors_set) / buttons_on_page)

        if page <= 0:
            page = 1
        elif page > pages_count:
            page = pages_count

        buttons_count = 0
        for exhibitor in sorted(exhibitors_set)[(page - 1) * buttons_on_page:page * buttons_on_page]:
            buttons_count += 1
            builder.button(text=exhibitor[0],
                           callback_data=ExhibitorInfo(exhibitor_id=exhibitor[1], full=full, letter=letter, page=page,
                                                       user_input=user_input))

        builder.adjust(1)

        if len(exhibitors) > buttons_on_page:
            builder.button(text="←", callback_data=ExhibitorSearchInfo(full=full, letter=letter, page=page - 1,
                                                                       user_input=user_input) if page > 1 else "inactive")
            builder.button(text=f"{page}/{pages_count}", callback_data="inactive")
            builder.button(text="→", callback_data=ExhibitorSearchInfo(full=full, letter=letter, page=page + 1,
                                                                       user_input=user_input) if page < pages_count else "inactive")
            builder.adjust(*[1 for _ in range(buttons_count)], 3)

    else:
        text = "По вашему запросу компаний не найдено"

    if list_type == "full":
        builder.row(InlineKeyboardButton(text="Вернуться в меню", callback_data="exhibitors_menu"))
    else:
        builder.row(InlineKeyboardButton(text="Продолжить поиск", callback_data=f"exhibitors_searching_{list_type}"),
                    InlineKeyboardButton(text="Отменить поиск", callback_data="exhibitors_menu"))

    return text, builder.as_markup()


# Inline клавиатура для вывода данных экспонента
def inline_exhibitors_details(exhibitor_details: dict, exhibitors_list_data: dict):
    builder = InlineKeyboardBuilder()
    full = exhibitors_list_data.get("full")
    letter = exhibitors_list_data.get("letter")
    page = exhibitors_list_data.get("page")
    user_input = exhibitors_list_data.get("user_input")

    booths_data = ''
    for elem in exhibitor_details['booths']:
        booths_data += f'Зал {elem.get("hall_number")} {elem.get("booth_number")} '

    text = (f"Компания: {exhibitor_details.get('name')}\n"
            f"Описание: {exhibitor_details.get('description')}\n"
            f"Телефон: {exhibitor_details.get('phone')}\n"
            f"Почта: {exhibitor_details.get('email')}\n"
            f"Сайт: {exhibitor_details.get('website')}\n"
            f"Расположение: {booths_data}")
    builder.button(text="Вернуться к списку экспонентов",
                   callback_data=ExhibitorSearchInfo(full=full, letter=letter, page=page, user_input=user_input))
    return text, builder.as_markup()
