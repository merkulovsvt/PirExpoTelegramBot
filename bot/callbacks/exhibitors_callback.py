from aiogram.filters.callback_data import CallbackData


class ExhibitorsSearchType(CallbackData, prefix="exhibitors_search_type"):
    search_type: str
    new_message: bool


class ExhibitorsList(CallbackData, prefix="exhibitors_list"):
    full: bool
    letter: str
    page: int
    user_input: str


class ExhibitorDetails(CallbackData, prefix="exhibitor_details"):
    exhibitor_id: int
    full: bool
    letter: str
    page: int
    user_input: str
