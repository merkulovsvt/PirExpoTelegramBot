from aiogram.filters.callback_data import CallbackData


class PartnersTypes(CallbackData, prefix="partners_types"):
    theme_id: str


class PartnersList(CallbackData, prefix="partners_list"):
    theme_id: str
    type_id: str


class PartnerDetails(CallbackData, prefix="partner_details"):
    partner_id: str
