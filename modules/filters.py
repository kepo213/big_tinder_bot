from aiogram import types
from modules.sql_func import read_by_name
from aiogram.dispatcher.filters import BoundFilter


class NotAllProfile(BoundFilter):
    key = 'not_all_profile'

    def __init__(self, not_all_profile):
        self.is_admin = not_all_profile

    async def check(self, message: types.Message):
        user_data = read_by_name(name='status', id_data=message.from_user.id)
        if str(user_data) == '[]':
            return False
        elif str(user_data[0][0]) == 'need_reg':
            return True
        else:
            return False
