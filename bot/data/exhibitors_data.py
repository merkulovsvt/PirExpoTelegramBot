from bot.utils.config import token
from bot.utils.scripts import request_json


async def get_exhibitors_letters() -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/exhibitor/filter"
    params = {"api_key": token}

    return await request_json(url=url, params=params)


async def get_exhibitors_list(full: bool | None, letter: str | None, user_input: str | None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/exhibitor/list"
    params = {"api_key": token}

    if full:
        pass
    elif letter:
        params["alphabet"] = letter
    elif user_input:
        params["name"] = user_input

    return await request_json(url=url, params=params)


async def get_exhibitor_details(exhibitor_id: int) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/exhibitor/{exhibitor_id}"
    params = {"api_key": token}

    return await request_json(url=url, params=params)
