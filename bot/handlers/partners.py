from aiogram import F, Router, types

from bot.data.partners_data import (get_partner_details, get_partners_list,
                                    get_themes_list)
from bot.keyboards.partners_boards import (inline_partner_details,
                                           inline_partner_type_list,
                                           inline_partners_list,
                                           inline_partners_themes)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выводу тем выставки через reply кнопку (только для ПИРа)
@router.message(LoggedIn(), F.text.lower() == "🤝 партнёры")
async def partners_themes_view(message: types.Message):
    themes_list = get_themes_list()

    text, keyboard = inline_partners_themes(themes_list=themes_list)
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выводу тем выставки через inline кнопку (только для ПИРа)
@router.callback_query(LoggedIn(), F.data == "themes_list")
async def callback_themes_view(callback: types.CallbackQuery):
    themes_list = get_themes_list()

    text, keyboard = inline_partners_themes(themes_list=themes_list)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу типов партнёров по теме через inline кнопку
@router.callback_query(LoggedIn(), F.data.startswith("theme_"))
async def callback_theme_types_list(callback: types.CallbackQuery):
    theme_id = callback.data.split("_")[1]

    partners_list = get_partners_list(theme_id=theme_id)

    text, keyboard = inline_partner_type_list(partners_list=partners_list, theme_id=theme_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу списка партнёров
@router.callback_query(LoggedIn(), F.data.startswith("partners_"))
async def callback_partners_list(callback: types.CallbackQuery):
    theme_id = callback.data.split("_")[1]
    type_id = callback.data.split("_")[2]

    partners_list = get_partners_list(theme_id=theme_id)

    text, keyboard = inline_partners_list(partners_list=partners_list, theme_id=theme_id, type_id=type_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных партнёра
@router.callback_query(LoggedIn(), F.data.startswith("partner_"))
async def callback_partners_list(callback: types.CallbackQuery):
    partner_id = callback.data.split("_")[1]

    partner_details = get_partner_details(partner_id=partner_id)

    text, keyboard = inline_partner_details(partner_details=partner_details)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()
