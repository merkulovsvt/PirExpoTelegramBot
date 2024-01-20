from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    logged_in = State()
    logged_out = State()


class Exhibitors(StatesGroup):
    searching = State()
