import requests

from bot.utils.config import token


async def post_user_data(chat_id: int, phone: str) -> None:
    url = "https://master.apiv2.pir.ru/tgbot/user/register"
    data = {"chat_id": chat_id, "phone": phone}
    params = {"api_key": token}

    requests.post(url, data=data, params=params)


def get_user_data(chat_id: int) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/user/me"
    params = {"chat_id": chat_id, "api_key": token}

    user_data = requests.get(url, params=params)
    return user_data.json()
