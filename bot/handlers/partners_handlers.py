from aiogram import F, Router, types
from aiogram.enums import ChatAction, ParseMode

from bot.callbacks.partners_callbacks import (PartnerDetails, PartnersList,
                                              PartnersTypes)
from bot.data.partners_data import (get_partner_details, get_partners_list,
                                    get_themes_list)
from bot.keyboards.partners_boards import (inline_partner_details,
                                           inline_partner_type_list,
                                           inline_partners_list,
                                           inline_partners_themes_list)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выводу списка тем выставки через reply кнопку (только для ПИРа)
@router.message(LoggedIn(), F.text.lower() == "🤝 партнёры")
async def partners_themes_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    themes_list = await get_themes_list()

    if len(themes_list) != 1:
        text, keyboard = inline_partners_themes_list(themes_list=themes_list)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        theme_id = str(themes_list[0].get('id'))

        partners_list = await get_partners_list(theme_id=theme_id)

        text, keyboard = inline_partner_type_list(partners_list=partners_list, theme_id=theme_id,
                                                  theme_filtration=False)
        await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выводу списка тем выставки через inline кнопку (только для ПИРа)
@router.callback_query(LoggedIn(), F.data == "partner_themes_list")
async def callback_partners_themes_list_view(callback: types.CallbackQuery):
    themes_list = await get_themes_list()

    if len(themes_list) != 1:
        text, keyboard = inline_partners_themes_list(themes_list=themes_list)
        await callback.message.answer(text=text, reply_markup=keyboard)
        await callback.answer()
    else:
        theme_id = str(themes_list[0].get('id'))

        partners_list = await get_partners_list(theme_id=theme_id)

        text, keyboard = inline_partner_type_list(partners_list=partners_list, theme_id=theme_id,
                                                  theme_filtration=False)
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        await callback.answer()


# Хендлер по выводу списка типов партнёров (Генеральный, информационный, ...)
@router.callback_query(LoggedIn(), PartnersTypes.filter())
async def callback_partners_types_list_view(callback: types.CallbackQuery, callback_data: PartnersTypes):
    theme_id = callback_data.theme_id
    partners_list = await get_partners_list(theme_id=theme_id)

    themes_list = await get_themes_list()
    if len(themes_list) != 1:
        theme_filtration = True
    else:
        theme_filtration = False

    text, keyboard = inline_partner_type_list(partners_list=partners_list, theme_id=theme_id,
                                              theme_filtration=theme_filtration)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу списка партнёров
@router.callback_query(LoggedIn(), PartnersList.filter())
async def callback_partners_list_view(callback: types.CallbackQuery, callback_data: PartnersList):
    theme_id = callback_data.theme_id
    type_id = callback_data.type_id

    partners_list = await get_partners_list(theme_id=theme_id)

    text, keyboard = inline_partners_list(partners_list=partners_list, theme_id=theme_id, type_id=type_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу данных партнёра
@router.callback_query(LoggedIn(), PartnerDetails.filter())
async def callback_partners_details_view(callback: types.CallbackQuery, callback_data: PartnerDetails):
    partner_id = callback_data.partner_id

    partner_details = await get_partner_details(partner_id=partner_id)

    text, keyboard = inline_partner_details(partner_details=partner_details)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await callback.answer()
