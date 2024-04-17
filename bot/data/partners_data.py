from bot.utils.scripts import request_json
from bot.utils.config import token


async def get_partners_list(theme_id: str | None):
    url = "https://master.apiv2.pir.ru/tgbot/partner/list"
    params = {"api_key": token}

    if theme_id:
        params['theme_id'] = theme_id

    return await request_json(url=url, params=params)


async def get_themes_list():
    url = "https://master.apiv2.pir.ru/tgbot/partner/filter"
    params = {"api_key": token}

    request = await request_json(url=url, params=params)
    return request['theme']


async def get_types_list():
    url = "https://master.apiv2.pir.ru/tgbot/partner/filter"
    params = {"api_key": token}

    request = await request_json(url=url, params=params)
    return request['types']


async def get_partner_details(partner_id: str):
    url = f"https://master.apiv2.pir.ru/tgbot/partner/{partner_id}"
    params = {"api_key": token}

    return await request_json(url=url, params=params)
