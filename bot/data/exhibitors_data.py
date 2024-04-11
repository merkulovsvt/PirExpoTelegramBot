import requests
from dotenv import load_dotenv

from bot.utils.config import token

load_dotenv()


def get_exhibitors_letters():
    url = "https://master.apiv2.pir.ru/tgbot/exhibitor/filter"
    params = {"api_key": token}

    letters = requests.get(url, params=params)
    return letters.json()


def get_exhibitors_list(full=None, letter=None, user_input=None):
    url = "https://master.apiv2.pir.ru/tgbot/exhibitor/list"
    params = {"api_key": token}

    if full:
        pass
    elif letter:
        params["alphabet"] = letter
    elif user_input:
        params["name"] = user_input

    exhibitors = requests.get(url, params=params)
    return exhibitors.json()


def get_exhibitor_details(exhibitor_id: int):
    url = f"https://master.apiv2.pir.ru/tgbot/exhibitor/{exhibitor_id}"
    params = {"api_key": token}

    exhibitor_details = requests.get(url, params=params)
    return exhibitor_details.json()
