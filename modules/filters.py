import datetime

from aiogram import types
from modules.sql_func import read_by_name, update_db
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


class CheckActivity(BoundFilter):
    key = 'active'

    def __init__(self, active):
        self.active = active

    async def check(self, message: types.Message):
        now = datetime.datetime.now()
        update_db(table="all_users", name="activity", data=now, id_data=message.from_user.id)
        update_db(table="chat_roll", name="status", data=0, id_data=message.from_user.id)
        return False


class CheckActivityCall(BoundFilter):
    key = 'active_call'

    def __init__(self, active_call):
        self.active_call = active_call

    async def check(self, call: types.CallbackQuery):
        now = datetime.datetime.now()
        update_db(table="all_users", name="activity", data=now, id_data=call.from_user.id)
        update_db(table="chat_roll", name="status", data=0, id_data=call.from_user.id)
        return False


class InChatRoll(BoundFilter):
    key = 'chat_roll'

    def __init__(self, chat_roll):
        self.chat_roll = chat_roll

    async def check(self, message: types.Message):
        chat_data = read_by_name(table='chat_roll', name='friend_id', id_data=message.from_user.id)
        if str(chat_data) == '[]':
            return False
        elif int(chat_data[0][0]) == 0:
            return False
        else:
            return True


class PremiumInChatRoll(BoundFilter):
    key = 'premium_in_chat'

    def __init__(self, premium_in_chat):
        self.premium_in_chat = premium_in_chat

    async def check(self, message: types.Message):
        premium_data = read_by_name(table='fast_info', name='premium', id_data=message.from_user.id)
        chat_data = read_by_name(table='chat_roll', name='friend_id', id_data=message.from_user.id)
        if str(chat_data) == '[]':
            return False
        elif int(chat_data[0][0]) == 0:
            return False
        else:
            if premium_data[0][0] == "1":
                return True
            else:
                return False
