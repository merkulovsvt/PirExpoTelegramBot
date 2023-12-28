import os

import requests
from bot.utils.func_tickets import get_ticket_type
from requests.auth import HTTPBasicAuth


# TODO надо ускорить
def get_orders(phone: str):
    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    payload = {"phone": phone}
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password), params=payload)
    orders = {}
    for order in r.json():
        if order["status"] == 3:
            for ticket in order["order_items"]:
                if not ticket["cancelled"]:
                    if order["id"] not in orders:
                        orders[order["id"]] = {"tickets": [], "invoice_url": None}
                    ticket_type = get_ticket_type(ticket["id"])
                    if ticket_type:
                        orders[order["id"]]["tickets"].append((ticket["id"], ticket_type))
            if order.get("invoice"):
                orders[order["id"]]["invoice_url"] = order["invoice"]["pdf_url"]
    return orders


def get_event_data():
    pass
