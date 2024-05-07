from aiogram.filters import Filter, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from bot.data.user_data import get_user_data
from bot.utils.config import exhibition_name
from bot.utils.states import User


class LoggedIn(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        if current_state == "User:logged_in":
            return True
        else:
            user_data = await get_user_data(chat_id=message.from_user.id)
            if user_data:
                await state.set_state(User.logged_in)
                return True
            else:
                return False
            # if user_data.get("detail") or user_data is {}:
            #     return False
            # else:
            #     await state.set_state(User.logged_in)
            #     return True


class LoggedOut(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        if current_state == "User:logged_out":
            return True
        else:
            user_data = await get_user_data(chat_id=message.from_user.id)
            if user_data:
                return False
            else:
                await state.set_state(User.logged_out)
                return True
            # if user_data.get("detail") or user_data is {}:
            #     await state.set_state(User.logged_out)
            #     return True
            # else:
            #     return False


class CheckReady(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        if current_state == "User:logged_in":
            return True
        elif current_state == "Exhibitors:searching":
            return False
        else:
            user_data = await get_user_data(message.from_user.id)
            if user_data.get("detail") or user_data is {}:
                return False
            else:
                await state.set_state(User.logged_in)
                return True


class PirExpo(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return exhibition_name == 'PIR'
