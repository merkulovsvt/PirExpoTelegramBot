from bot.utils.config import server_url, bot_token
from bot.utils.scripts import get_json_request


async def get_exhibitors_letters() -> dict:
    url = server_url + "/tgbot/exhibitor/filter"
    params = {"api_key": bot_token}

    return await get_json_request(url=url, params=params)


async def get_exhibitors_list(full: bool | None, letter: str | None, user_input: str | None) -> dict:
    url = server_url + "/tgbot/exhibitor/list"
    params = {"api_key": bot_token}

    if full:
        pass
    elif letter:
        params["alphabet"] = letter
    elif user_input:
        params["name"] = user_input

    return await get_json_request(url=url, params=params)


async def get_exhibitor_details(exhibitor_id: int) -> dict:
    url = server_url + f"/tgbot/exhibitor/{exhibitor_id}"
    params = {"api_key": bot_token}

    return await get_json_request(url=url, params=params)
