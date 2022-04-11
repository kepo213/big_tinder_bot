
from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserProfile
from modules.functions.check_photo import search_face
from modules.keyboards import user_couples_kb
from modules.sql_func import update_db, read_by_name, join_profile_all
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


def find_person(user_id: int):
    user_data = read_by_name(name='longitude, latitude, search_range', id_data=user_id)[0]
    x_left = float(user_data[]) + 0.0088 * int(i[7])
    x_right = float(user_data) - 0.0088 * int(i[7])
    y_up = float(user_data) + 0.015187 * int(i[7])
    y_down = float(user_data) - 0.015187 * int(i[7])
    finded_user_id = 0
    text = '0'
    return finded_user_id, text


# Profile menu
@dp.message_handler(commands=['love'], state='*')
@dp.message_handler(Text(equals='👩‍❤️‍👨 Найти пару', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    find_person()
    await message.answer_photo(f'Text', reply_markup=user_couples_kb(user_id=message.from_user.id))


# Profile menu
@dp.callback_query_handler(state=UserProfile.name, text='close_it')
async def start_menu(call: types.CallbackQuery):
    # Send main profile text
    pass
