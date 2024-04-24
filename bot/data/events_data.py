from bot.utils.config import server_url, bot_token
from bot.utils.scripts import get_json_request


async def get_events_list(chat_id: int | None, event_date: str | None, theme_id: str | None) -> dict:
    url = server_url + "/tgbot/event/list"
    params = {"api_key": bot_token}

    if chat_id:
        params["chat_id"] = chat_id

    if event_date:
        params["date"] = event_date

    if theme_id:
        params["theme"] = theme_id

    return await get_json_request(url=url, params=params)


async def get_event_themes(chat_id: int | None) -> dict:
    url = server_url + "/tgbot/event/filter"
    params = {"api_key": bot_token}

    if chat_id:
        params["chat_id"] = chat_id

    return await get_json_request(url=url, params=params)


async def get_event_data(event_id: str):
    url = server_url + f"/tgbot/event/{event_id}"
    params = {"api_key": bot_token, 'id': event_id}

    return await get_json_request(url=url, params=params)
