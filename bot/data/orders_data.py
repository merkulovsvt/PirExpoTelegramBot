import json
import os

import requests
from requests.auth import HTTPBasicAuth

from bot.utils.config import login, password


def get_orders_list(chat_id: int) -> dict:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"chat_id": chat_id}
    #
    # orders_list = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    # return orders_list.json()

    json_path = os.path.join(os.getcwd(), 'static', 'orders.json')
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_order_details(order_id: str) -> dict:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"order_id": order_id}
    #
    # order_data = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    # return order_details.json()
    json_path = os.path.join(os.getcwd(), 'static', 'orders.json')
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data
