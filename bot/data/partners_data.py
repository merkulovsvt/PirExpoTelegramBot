from bot.utils.config import server_url, token
from bot.utils.scripts import get_json_request


async def get_partners_list(theme_id: str | None):
    url = server_url + "/tgbot/partner/list"
    params = {"api_key": token}

    if theme_id:
        params['theme_id'] = theme_id

    return await get_json_request(url=url, params=params)


async def get_themes_list():
    url = server_url + "/tgbot/partner/filter"
    params = {"api_key": token}

    request = await get_json_request(url=url, params=params)
    return request['theme']


async def get_types_list():
    url = server_url + "/tgbot/partner/filter"
    params = {"api_key": token}

    request = await get_json_request(url=url, params=params)
    return request['types']


async def get_partner_details(partner_id: str):
    url = server_url + f"/tgbot/partner/{partner_id}"
    params = {"api_key": token}

    return await get_json_request(url=url, params=params)
