from aiogram.filters.callback_data import CallbackData


class EventsThemes(CallbackData, prefix="events_themes"):
    events_type: str


class EventsList(CallbackData, prefix="events_list"):
    theme_id: str


class EventDetails(CallbackData, prefix="event_details"):
    theme_id: str
    event_id: str


class EventPrint(CallbackData, prefix="event_print"):
    ticket_type_id: str
