import requests
from dotenv import load_dotenv

from bot.utils.config import token

load_dotenv()


def get_partners_list(theme_id=None):
    url = "https://master.apiv2.pir.ru/tgbot/partner/list"
    params = {"api_key": token}

    if theme_id:
        params['theme_id'] = theme_id

    partners = requests.get(url, params=params)
    return partners.json()


def get_themes_list():
    url = "https://master.apiv2.pir.ru/tgbot/partner/filter"
    params = {"api_key": token}

    themes_and_types = requests.get(url, params=params)
    return themes_and_types.json()["theme"]


def get_types_list():
    url = "https://master.apiv2.pir.ru/tgbot/partner/filter"
    params = {"api_key": token}

    themes_and_types = requests.get(url, params=params)
    return themes_and_types.json()["types"]


def get_partner_details(partner_id: str):
    url = f"https://master.apiv2.pir.ru/tgbot/partner/{partner_id}"
    params = {"api_key": token}

    partner_details = requests.get(url, params=params)
    return partner_details.json()
