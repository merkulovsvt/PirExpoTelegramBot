import aiohttp
from aiogram import F, Router, types
from aiogram.enums import ChatAction, ParseMode

from bot.callbacks.events_callbacks import (EventDetails, EventPrint,
                                            EventsList, EventsThemes)
from bot.data.events_data import (get_event_data, get_event_themes,
                                  get_events_list)
from bot.data.tickets_data import get_ticket_list_by_event
from bot.keyboards.events_boards import (inline_event_categories,
                                         inline_events_details,
                                         inline_events_list,
                                         inline_events_themes)
from bot.utils.filters import LoggedIn

router = Router()


# Хендлер по выбору типа мероприятий по reply кнопке
@router.message(LoggedIn(), F.text.lower() == "🎉 мероприятия")
async def events_type_view(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    text, keyboard = inline_event_categories()
    await message.answer(text=text, reply_markup=keyboard)


# Хендлер по выбору типа мероприятий по inline кнопке
@router.callback_query(LoggedIn(), F.data == "event_categories_list")
async def callback_events_type_view(callback: types.CallbackQuery):
    text, keyboard = inline_event_categories()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выбору темы мероприятия (Кофе, Отель, ...)
@router.callback_query(LoggedIn(), EventsThemes.filter())
async def callback_events_theme_view(callback: types.CallbackQuery, callback_data: EventsThemes):
    events_type = callback_data.events_type

    if events_type == "my":
        event_themes = await get_event_themes(chat_id=callback.message.chat.id)
    else:
        event_themes = await get_event_themes(chat_id=None)

    text, keyboard = inline_events_themes(event_themes=event_themes, events_type=events_type)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу списка мероприятия
@router.callback_query(LoggedIn(), EventsList.filter())
async def callback_events_list_view(callback: types.CallbackQuery, callback_data: EventsList):
    theme_id = callback_data.theme_id

    events = await get_events_list(chat_id=callback.message.chat.id, event_date=None, theme_id=theme_id)

    text, keyboard = inline_events_list(events=events, theme_id=theme_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


# Хендлер по выводу деталей мероприятия
@router.callback_query(LoggedIn(), EventDetails.filter())
async def callback_events_details_view(callback: types.CallbackQuery, callback_data: EventDetails):
    theme_id = callback_data.theme_id
    event_id = callback_data.event_id

    event_data = await get_event_data(event_id=event_id)

    text, keyboard = inline_events_details(event_data=event_data, theme_id=theme_id)
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await callback.answer()


# Хендлер по отправке pdf билета по ticket_type
@router.callback_query(LoggedIn(), EventPrint.filter())
async def callback_events_print(callback: types.CallbackQuery,callback_data:EventPrint):
    ticket_type_id = callback_data.ticket_type_id

    ticket_list = await get_ticket_list_by_event(chat_id=callback.message.chat.id, ticket_type_id=ticket_type_id)

    for ticket in ticket_list:

        url = ticket["pdf_url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.read()
                    await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id,
                                                                action=ChatAction.UPLOAD_DOCUMENT)

                    await callback.bot.send_document(callback.message.chat.id, document=types.BufferedInputFile(
                        file=result, filename=f'Билет #{ticket["id"]}.pdf'),
                                                     caption=f"Билет #{ticket['id']} на "
                                                             f"мероприятие\n\"{ticket['ticket_type']['name']}\"")
                else:
                    await callback.message.reply(
                        text=f"К сожалению, не можем прислать билет №{ticket['id']} на"
                             f"\"мероприятие\n\"{ticket['ticket_type']['name']}\"")

        await callback.answer()
