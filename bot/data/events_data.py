import requests

from bot.utils.config import token


def get_events_list(chat_id=None, date=None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/event/list"
    params = {"api_key": token}

    if chat_id:
        params["chat_id"] = chat_id

    if date:
        params["date"] = date

    events_list = requests.get(url, params=params)

    if type(events_list.json()) == list:
        return events_list.json()
    elif events_list.json().get("detail"):
        return {}


def get_event_themes(chat_id=None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/event/filter"
    params = {"api_key": token}

    if chat_id:
        params["chat_id"] = chat_id

    events_list = requests.get(url, params=params)
    return events_list.json()


def get_order_details(order_id: str) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/order/{order_id}"
    params = {"api_key": token}

    order_details = requests.get(url, params=params)
    return order_details.json()
