from bot.utils.config import server_url, bot_token
from bot.utils.scripts import get_json_request, post_request


async def post_user_data(chat_id: int, phone: str) -> None:
    url = server_url + "/tgbot/user/register"
    data = {"chat_id": chat_id, "phone": phone}
    params = {"api_key": bot_token}

    await post_request(url=url, params=params, data=data)


async def get_user_data(chat_id: int) -> dict:
    url = server_url + "/tgbot/user/me"
    params = {"chat_id": chat_id, "api_key": bot_token}
    return await get_json_request(url=url, params=params)
