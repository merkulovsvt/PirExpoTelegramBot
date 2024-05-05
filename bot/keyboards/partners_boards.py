from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.partners_callbacks import (PartnerDetails, PartnersList,
                                              PartnersTypes)


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
def inline_partner_type_list(partners_list: dict, theme_id: str, theme_filtration: bool):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип партнёра:"

    type_set = set()
    for partner in partners_list:
        type_set.add((partner["type"]["name"], str(partner["type"]["id"])))

    for type in sorted(type_set, key=lambda x: x[0]):
        builder.button(text=type[0], callback_data=PartnersList(theme_id=theme_id, type_id=type[1]))

    if theme_filtration:
        builder.button(text="🤝 Вернуться к выбору выставки", callback_data="partner_themes_list")

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка партнёров
def inline_partners_list(partners_list: dict, theme_id: str, type_id: str):
    builder = InlineKeyboardBuilder()
    text = "Список партнёров:"

    partner_set = set()
    for partner in partners_list:
        if str(partner["type"]["id"]) == type_id:
            partner_set.add((partner["logo"]["order"], partner["name"], str(partner["id"])))
    # print(partner_set)
    for partner in sorted(partner_set, key=lambda x: x[0]):
        builder.button(text=partner[1], callback_data=PartnerDetails(partner_id=partner[2]))

    builder.button(text="🤝 Вернуться к выбору типов", callback_data=PartnersTypes(theme_id=theme_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()


# Inline клавиатура для вывода данных партнёров
def inline_partner_details(partner_details: dict):
    builder = InlineKeyboardBuilder()

    theme_id = str(partner_details["themes"][0]["id"])
    type_id = str(partner_details["type"]["id"])

    text = ''

    if partner_details.get('name'):
        text += f"<b>Компания</b>: {partner_details.get('name')}\n\n"

    if partner_details.get('status'):
        text += f"<b>Статус</b>: {partner_details.get('status')}\n\n"
    elif partner_details.get('type'):
        types_set = set()

        if type(partner_details.get('type')) == list:
            for partner_type in partner_details.get('type'):
                types_set.add(partner_type.get("name"))
        elif type(partner_details.get('type')) == dict:
            types_set.add(partner_details.get('type').get("name"))

        types_string = ", ".join(map(str, types_set))
        text += f"<b>Статус</b>: {types_string}\n\n"

    if partner_details.get('description'):
        text += f"<b>Описание</b>: {partner_details.get('description')}\n\n"

    if partner_details.get('themes'):
        themes_set = set()
        for theme in partner_details.get('themes'):
            themes_set.add(theme.get("name"))
        themes_string = ", ".join(map(str, themes_set))
        text += f"<b>Тематики</b>: {themes_string}\n\n"

    # if partner_details.get('contact'):
    #     text += f"<b>Телефон</b>: {partner_details.get('contact')}\n\n"

    if partner_details.get('website'):
        text += f"<b>Сайт</b>: {partner_details.get('website')}\n\n"

    text = text.replace("<br>", "\n")

    builder.button(text="🤝 Вернуться к списку партнёров",
                   callback_data=PartnersList(theme_id=theme_id, type_id=type_id))

    builder.adjust(1, repeat=True)
    return text, builder.as_markup()
