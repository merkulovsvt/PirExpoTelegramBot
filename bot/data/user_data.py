import requests
from requests.auth import HTTPBasicAuth

from bot.utils.config import login, password


def post_user_data(chat_id: int, phone_number: str, logged_in: bool) -> None:
    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    params = {"chat_id": chat_id, "phone_number": phone_number, "logged_in": logged_in}

    requests.post(url, auth=HTTPBasicAuth(login, password), params=params)


def get_user_data(chat_id: int) -> dict:
    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    params = {"chat_id ": chat_id}

    tickets_list = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    return tickets_list.json()
