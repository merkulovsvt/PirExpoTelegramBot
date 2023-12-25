from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    logged_out = State()
    logged_in = State()
