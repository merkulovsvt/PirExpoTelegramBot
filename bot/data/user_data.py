from bot.utils.config import token
from bot.utils.scripts import get_request, post_request


async def post_user_data(chat_id: int, phone: str) -> None:
    url = "https://master.apiv2.pir.ru/tgbot/user/register"
    data = {"chat_id": chat_id, "phone": phone}
    params = {"api_key": token}

    await post_request(url=url, params=params, data=data)


async def get_user_data(chat_id: int) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/user/me"
    params = {"chat_id": chat_id, "api_key": token}
    return await get_request(url=url, params=params)
