from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.partners_callbacks import PartnersTypes, PartnersList, PartnerDetails


# Inline клавиатура для вывода тем выставки
def inline_partners_themes_list(themes_list: list):
    builder = InlineKeyboardBuilder()
    text = "Выберите выставку:"

    for theme in sorted(themes_list, key=lambda x: x["name"]):
        theme_id = str(theme['id'])
        builder.button(text=theme["name"], callback_data=PartnersTypes(theme_id=theme_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода типа партнёров
def inline_partner_type_list(partners_list: dict, theme_id: str):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип партнёра:"

    type_set = set()
    for partner in partners_list:
        type_set.add((partner["type"]["name"], str(partner["type"]["id"])))

    for type in sorted(type_set, key=lambda x: x[0]):
        builder.button(text=type[0], callback_data=PartnersList(theme_id=theme_id, type_id=type[1]))

    builder.button(text="Вернуться к выбору выставки", callback_data="partner_themes_list")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка партнёров
def inline_partners_list(partners_list: dict, theme_id: str, type_id: str):
    builder = InlineKeyboardBuilder()
    text = "Список партнёров:"

    partner_set = set()
    for partner in partners_list:
        if str(partner["type"]["id"]) == type_id:
            partner_set.add((partner["name"], str(partner["id"])))

    for partner in sorted(partner_set, key=lambda x: x[0]):
        builder.button(text=partner[0], callback_data=PartnerDetails(partner_id=partner[1]))

    builder.button(text="Вернуться к выбору типов", callback_data=PartnersTypes(theme_id=theme_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода данных партнёров
def inline_partner_details(partner_details: dict):
    builder = InlineKeyboardBuilder()

    theme_id = str(partner_details["themes"][0]["id"])
    type_id = str(partner_details["type"]["id"])

    text = (f"{partner_details['name']}\n" + f"{partner_details['status']}\n" +
            f"{partner_details['description']}\n" + f"{partner_details['contact']}\n")

    if partner_details.get("website"):
        builder.button(text="Ссылка на сайт партнёра", url=partner_details["website"])

    builder.button(text="Вернуться к списку партнёров", callback_data=PartnersList(theme_id=theme_id, type_id=type_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()
