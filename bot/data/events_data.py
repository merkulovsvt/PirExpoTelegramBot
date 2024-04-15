import requests

from bot.utils.config import token


def get_events_list(chat_id=None, date=None, theme_id=None) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/event/list"
    params = {"api_key": token}

    if chat_id:
        params["chat_id"] = chat_id

    if date:
        params["date"] = date

    if theme_id:
        params["theme"] = theme_id

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


def get_event_data(event_id: str):
    url = f"https://master.apiv2.pir.ru/tgbot/event/{event_id}"
    params = {"api_key": token, 'id': event_id}

    event_data = requests.get(url, params=params)

    if event_data.status_code == 200:
        return event_data.json()
    else:
        return {}
