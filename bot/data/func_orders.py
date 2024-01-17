import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from bot.data.func_tickets import get_ticket_type

load_dotenv()


# TODO надо ускорить
def get_orders(phone: str):
    print(phone)
    url = "https://master.apiv2.pir.ru/api/v1/order/list"
    params = {"phone": phone}
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    orders = {}
    for order in r.json():
        if order["status"] == 3:
            for ticket in order["order_items"]:
                if not ticket["cancelled"]:
                    if order["id"] not in orders:
                        orders[str(order["id"])] = {"tickets": [], "invoice_url": None}
                    ticket_type = get_ticket_type(ticket["id"])
                    if ticket_type:
                        orders[str(order["id"])]["tickets"].append((str(ticket["id"]), ticket_type))
            if order.get("invoice"):
                orders[str(order["id"])]["invoice_url"] = order["invoice"]["pdf_url"]
    print(orders)
    return orders


def get_event_data():
    pass
