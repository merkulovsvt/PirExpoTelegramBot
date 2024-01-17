import json
import os

import requests
from requests.auth import HTTPBasicAuth

from bot.utils.config import login, password


def get_tickets_list(chat_id: int, *order_id) -> dict:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"chat_id": chat_id}
    #
    # if order_id:
    #     params["order_id"] = order_id
    #
    # tickets_list = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    # return tickets_list.json()

    json_path = os.path.join(os.getcwd(), 'static', 'tickets.json')
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def get_ticket_data(ticket_id: str) -> dict:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"ticket_id": ticket_id}
    #
    # tickets_list = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    # return tickets_list.json()
    json_path = os.path.join(os.getcwd(), 'static', 'ticket_data.json')
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data
