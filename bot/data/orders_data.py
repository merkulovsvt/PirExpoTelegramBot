import requests

from bot.utils.config import token


def get_orders_list(chat_id: int) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/order/list"
    params = {"chat_id": chat_id, "api_key": token}

    orders_list = requests.get(url, params=params)
    return orders_list.json()


def get_order_details(order_id: str) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/order/{order_id}"
    params = {"api_key": token}

    order_details = requests.get(url, params=params)
    return order_details.json()


def tickets_status_check(order: dict) -> bool:
    for ticket in order["tickets"]:
        if ticket["status"] == "2":
            return True
    return False
