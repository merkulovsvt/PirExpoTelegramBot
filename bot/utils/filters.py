from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from bot.data.user_data import get_user_data
from bot.utils.states import User


class LoggedIn(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:

        if await state.get_state() == "User:logged_in":
            return True
        else:
            user_data = get_user_data(message.chat.id)
            if user_data["state"] == "User:logged_in" and user_data["phone_number"]:
                await state.set_state(User.logged_in)
                return True
            else:
                return False


class LoggedOut(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        print(1)
        if await state.get_state() == "User:logged_out":
            return True
        else:
            user_data = get_user_data(message.chat.id)
            if user_data["state"] == "User:logged_out":
                await state.set_state(User.logged_out)
                return True
            else:
                return False
