from bot.utils.config import token
from bot.utils.scripts import get_request


async def get_tickets_list(chat_id: int, order_id: str) -> dict:
    url = "https://master.apiv2.pir.ru/tgbot/ticket/list"
    params = {"chat_id": chat_id, "api_key": token}

    if order_id != "*":
        params["order_id"] = order_id

    return await get_request(url=url, params=params)


async def get_ticket_list_by_event(chat_id: int, ticket_type_id: str) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/ticket/list"
    params = {"api_key": token, "chat_id": chat_id, "ticket_type": ticket_type_id}

    return await get_request(url=url, params=params)


async def get_ticket_details(ticket_id: str) -> dict:
    url = f"https://master.apiv2.pir.ru/tgbot/ticket/{ticket_id}"
    params = {"ticket_id": ticket_id, "api_key": token}

    return await get_request(url=url, params=params)


def tickets_status_check(tickets: dict) -> bool:
    for ticket in tickets:
        if ticket["status"] == "2":
            return True
    return False
