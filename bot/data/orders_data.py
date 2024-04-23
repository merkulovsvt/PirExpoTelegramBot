from bot.utils.config import server_url, token
from bot.utils.scripts import get_json_request


async def get_orders_list(chat_id: int) -> dict:
    url = server_url + "/tgbot/order/list"
    params = {"chat_id": chat_id, "api_key": token}

    return await get_json_request(url=url, params=params)


async def get_order_details(order_id: str) -> dict:
    url = server_url + f"/tgbot/order/{order_id}"
    params = {"api_key": token}

    return await get_json_request(url=url, params=params)


def tickets_status_check(order: dict) -> bool:
    for ticket in order["tickets"]:
        if ticket["status"] == "2":
            return True
    return False
