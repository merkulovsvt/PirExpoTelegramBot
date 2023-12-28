import json
import os

import requests
from requests.auth import HTTPBasicAuth


def load_exhibitors():
    json_path = os.getcwd() + "\\bot\\static\\exhibitors_data.json"
    try:
        with open(json_path, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                return data
            except Exception:
                return get_exhibitors(json_path)
    except FileNotFoundError:
        return get_exhibitors(json_path)


def get_exhibitors(json_path: str):
    url = "https://master.apiv2.pir.ru/api/v1/participation/list"
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    exhibitors = {}
    r = requests.get(url, auth=HTTPBasicAuth(login, password))
    for exhibitor in r.json():
        exhibitors[exhibitor["id"]] = get_exhibitor_data(exhibitor["id"])

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(exhibitors, json_file, ensure_ascii=False)
    return exhibitors


def get_exhibitor_data(exhibitor_id: int):
    url = f"https://master.apiv2.pir.ru/api/v1/participation/{exhibitor_id}"
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    r = requests.get(url, auth=HTTPBasicAuth(login, password))
    data = r.json()
    return {"name": data["name"], "description": data["description"], "booth_data": get_booth_data(data["booths"])}


def get_booth_data(booths: list):
    booth_data = {}
    for booth in booths:
        booth_data[booth["id"]] = {"booth_number": booth["booth_number"], "hall_number": booth["hall_number"]}
    return booth_data
