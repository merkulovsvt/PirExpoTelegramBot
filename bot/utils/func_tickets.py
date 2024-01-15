import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


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


# TODO это не ticket_type это из is_event ПОМЕНЯТЬ!
def get_tickets_list(from_order: bool, orders: dict, ticket_type: str, order_id=-1) -> list:
    tickets_list = []

    if from_order:
        orders_pool = [order_id]
    else:
        orders_pool = orders

    for o_id in orders_pool:
        for t_id, t_type in orders[o_id]["tickets"]:
            if t_type == ticket_type:
                if ticket_type == "entry":
                    tickets_list.append(t_id)
                elif ticket_type == "event":
                    # TODO разделение по датам
                    tickets_list.append(t_id)

    return tickets_list
