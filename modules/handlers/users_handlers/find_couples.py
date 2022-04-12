import math
from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserProfile
from modules.functions.check_photo import search_face
from modules.keyboards import user_couples_kb
from modules.sql_func import update_db, read_by_name, search_geo
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


def find_person(user_id: int):
    user_data = read_by_name(name='longitude, latitude, search_range, search_sex', id_data=user_id, table='fast_info')[0]
    lust_couple_id = read_by_name(name='lust_couple_id', id_data=user_id, table='couples')[0][0]
    # keep params for search
    y_up = float(user_data[0]) + 0.0089 * int(user_data[2])
    y_down = float(user_data[0]) - 0.0089 * int(user_data[2])
    x_right = float(user_data[1]) + 0.015187 * int(user_data[2])
    x_left = float(user_data[1]) - 0.015187 * int(user_data[2])
    search_sex = user_data[3]
    finded_user = (search_geo(y_down, y_up, x_right, x_left, search_sex=search_sex, lust_id=lust_couple_id))
    if str(finded_user) == '[]':
        finded_user = (search_geo(y_down, y_up, x_right, x_left, search_sex=search_sex, lust_id=0))
        update_db(table='couples', name='lust_couple_id', data=0, id_data=user_id)
    else:
        update_db(table='couples', name='lust_couple_id', data=finded_user[0][0], id_data=user_id)
    print(finded_user)
    text = '0'
    return finded_user, text


# Profile menu
@dp.message_handler(commands=['love'], state='*')
@dp.message_handler(Text(equals='👩‍❤️‍👨 Найти пару', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    find_person(message.from_user.id)
    # await message.answer_photo(f'Text', reply_markup=user_couples_kb(user_id=message.from_user.id))


# Profile menu
@dp.callback_query_handler(state=UserProfile.name, text='close_it')
async def start_menu(call: types.CallbackQuery):
    # Send main profile text
    pass
