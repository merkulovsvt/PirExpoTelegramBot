import os

import requests
from aiogram.fsm.state import State, StatesGroup
from requests.auth import HTTPBasicAuth


class User(StatesGroup):
    logged_out = State()
    logged_in = State()


def orders_get(phone: str):
    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    payload = {"phone": phone}
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password), params=payload)
    orders = {}
    for order in r.json():
        for order_item in order["order_items"]:
            if order["id"] not in orders:
                orders[order["id"]] = {'ticket_ids': [], 'invoice_url': None}
                if not order_item["cancelled"]:
                    orders[order["id"]]['ticket_ids'].append(order_item["id"])
        if order["invoice"]:
            orders[order["id"]]['invoice_url'] = order["invoice"]["pdf_url"]
    return orders


def ticket_data(ticket_ids: list):
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    tickets_data = {}

    for ticket_id in ticket_ids:
        url = f"https://master.apiv2.pir.ru/api/v1/ticket/{ticket_id}/print"
        r = requests.get(url, auth=HTTPBasicAuth(login, password))
        tickets_data[ticket_id] = {''}

    return r.status_code
