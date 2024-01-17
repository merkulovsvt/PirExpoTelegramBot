import json
import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


def load_events():
    json_path = os.path.join(os.getcwd(), 'static', 'events_data.json')
    try:
        with open(json_path, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                return data
            except Exception:
                return get_events(json_path)
    except FileNotFoundError:
        return get_events(json_path)


def get_events(json_path: str):
    url = "https://master.apiv2.pir.ru/api/v1/event/list"
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    events = {}
    r = requests.get(url, auth=HTTPBasicAuth(login, password))
    for event in r.json():
        events[event["id"]] = event

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(events, json_file, ensure_ascii=False)
    return events

# def get_event_data(event: dict):
#     return {"name": event["name"], "description": data["description"], "booth_data": get_booth_data(data["booths"])}
