import os

import requests
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


def get_ticket_type(ticket_id: int):
    url = f"https://master.apiv2.pir.ru/api/v1/ticket/{ticket_id}"
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password))
    data = r.json().get("ticket_type")
    if data:
        if data["is_event"]:
            return "event"
        else:
            return "entry"
    return None


def get_ticket_list(from_order: bool, orders: dict, ticket_type: str, order_id=-1) -> list:
    tickets_list = []
    if from_order:
        for t_id, t_type in orders[order_id]["tickets"]:
            if t_type == ticket_type:
                tickets_list.append(t_id)
    else:
        for o_id in orders:
            for t_id, t_type in orders[o_id]["tickets"]:
                if t_type == ticket_type:
                    tickets_list.append(t_id)

    return tickets_list
