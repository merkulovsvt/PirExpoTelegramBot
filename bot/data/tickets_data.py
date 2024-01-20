import requests

from bot.utils.config import token


def get_tickets_list(chat_id: int, order_id: str) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/ticket/list"
    params = {"chat_id": chat_id, "api_key": token}

    if order_id != "*":
        params["order_id"] = order_id

    tickets_list = requests.get(url, params=params)
    return tickets_list.json()


def get_ticket_details(ticket_id: str) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/ticket/{ticket_id}"
    params = {"ticket_id": ticket_id, "api_key": token}

    tickets_list = requests.get(url, params=params)
    return tickets_list.json()
