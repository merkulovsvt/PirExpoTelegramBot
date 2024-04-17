from bot.utils.config import token
from bot.utils.scripts import request_json


async def get_events_list(chat_id: int | None, event_date: str | None, theme_id: str | None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/event/list"
    params = {"api_key": token}

    if chat_id:
        params["chat_id"] = chat_id

    if event_date:
        params["date"] = event_date

    if theme_id:
        params["theme"] = theme_id

    return await request_json(url=url, params=params)


async def get_event_themes(chat_id: int | None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/event/filter"
    params = {"api_key": token}

    if chat_id:
        params["chat_id"] = chat_id

    return await request_json(url=url, params=params)


async def get_event_data(event_id: str):
    url = f"https://master.apiv2.pir.ru/tgbot/event/{event_id}"
    params = {"api_key": token, 'id': event_id}

    return await request_json(url=url, params=params)
