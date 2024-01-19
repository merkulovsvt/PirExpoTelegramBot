import json
import os


async def put_user_data(chat_id: int, state: str, phone_number=None) -> None:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"chat_id": chat_id, "phone_number": phone_number, "state": state}
    #
    # requests.post(url, auth=HTTPBasicAuth(login, password), params=params)
    zaza = 1


def get_user_data(chat_id: int) -> dict:
    # url = "https://master.apiv2.pir.ru/api/v1/order/list"
    # params = {"chat_id ": chat_id}
    #
    # tickets_list = requests.get(url, auth=HTTPBasicAuth(login, password), params=params)
    # return tickets_list.json()

    json_path = os.path.join(os.getcwd(), 'static', 'user_data.json')
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data
