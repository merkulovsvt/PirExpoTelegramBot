from aiogram.utils.keyboard import InlineKeyboardBuilder


# Inline клавиатура для вывода тем выставки
def inline_partners_themes(themes_list: list):
    builder = InlineKeyboardBuilder()
    text = "Выберите выставку:"

    for theme in sorted(themes_list, key=lambda x: x["name"]):
        builder.button(text=theme["name"], callback_data=f"theme_{theme['id']}")

    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода типа партнёров
def inline_partner_type_list(partners_list: dict, theme_id: str):
    builder = InlineKeyboardBuilder()
    text = "Выберите тип партнёра:"

    type_set = set()
    for partner in partners_list:
        type_set.add((partner["type"]["name"], str(partner["type"]["id"])))

    for type in sorted(type_set):
        builder.button(text=type[0], callback_data=f"partners_{theme_id}_{type[1]}")

    builder.button(text="Вернуться к выбору выставки", callback_data=f"themes_list")
    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода списка партнёров
def inline_partners_list(partners_list: dict, theme_id: str, type_id: str):
    builder = InlineKeyboardBuilder()
    text = "Список партнёров:"

    partner_set = set()
    for partner in partners_list:
        if str(partner["type"]["id"]) == type_id:
            partner_set.add((partner["name"], partner["id"]))

    for partner in sorted(partner_set):
        builder.button(text=partner[0], callback_data=f"partner_{partner[1]}")

    builder.button(text="Вернуться к выбору типов", callback_data=f"theme_{theme_id}")
    builder.adjust(1)
    return text, builder.as_markup()


# Inline клавиатура для вывода данных партнёров
def inline_partner_details(partner_details: dict):
    builder = InlineKeyboardBuilder()

    theme_id = partner_details["themes"][0]["id"]
    type_id = partner_details["type"]["id"]

    text = (f"{partner_details['name']}\n" + f"{partner_details['status']}\n" +
            f"{partner_details['description']}\n" + f"{partner_details['contact']}\n")

    if partner_details.get("website"):
        builder.button(text="Ссылка на сайт партнёра", url=partner_details["website"])

    builder.button(text="Вернуться к списку партнёров", callback_data=f"partners_{theme_id}_{type_id}")
    builder.adjust(1)
    return text, builder.as_markup()
