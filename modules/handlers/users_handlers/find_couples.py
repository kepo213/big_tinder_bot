import math
from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserProfile
from modules.functions.check_photo import search_face
from modules.keyboards import user_couples_kb
from modules.sql_func import update_db, read_by_name, search_person, join_profile_all
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


def create_text(user_id: int, premium_finder: str):
    user_data = join_profile_all(id_data=user_id)[0]

    if str(user_data[7]) == "0":
        emoji = ''
    else:
        emoji = user_data[7]

    if str(user_data[5]) == "0":
        good = '✖️ Фото не подтверждено'
    else:
        good = '✅ Фото подтверждено'

    if str(user_data[10]) == "0":
        premium = ''
    else:
        premium = '💎'
    if premium_finder == '0':
        insta = ''
    else:
        if str(user_data[9]) == "0":
            insta = ''
        else:
            insta = f'📸<a href="https://instagram.com/{user_data[9]}">Instagram</a>\n'

    if str(user_data[8]) == "0":
        zodiac = ''
    else:
        zodiac = f'{user_data[8]}\n'

    if str(user_data[3]) == "0":
        city = ''
    else:
        city = f'🗺{user_data[3]}\n'

    if str(user_data[6]) == "0":
        description = ''
    else:
        description = f'📝{user_data[6]}\n'

    name = user_data[1]
    age = user_data[2]
    # Собираем текст
    text = f'{emoji}{name}, {age} {premium}\n\n' \
           f'{good}\n' \
           f'{insta}{zodiac}{city}{description}'
    return text


def find_person(user_id: int):
    user_data = read_by_name(name='longitude, latitude, search_range, search_sex, premium, age_min, age_max',
                             id_data=user_id, table='fast_info')[0]
    lust_couple_id = read_by_name(name='id', id_data=user_id, table='couples')[0][0]
    # keep params for search
    y_up = float(user_data[0]) + 0.0089 * int(user_data[2])
    y_down = float(user_data[0]) - 0.0089 * int(user_data[2])
    x_right = float(user_data[1]) + 0.015187 * int(user_data[2])
    x_left = float(user_data[1]) - 0.015187 * int(user_data[2])
    age_min = int(user_data[5])
    age_max = int(user_data[6])
    search_sex = user_data[3]
    finded_user = (search_person(x_left=y_down, x_right=y_up, y_up=x_right, y_down=x_left,
                                 search_sex=search_sex, lust_id=lust_couple_id, age_min=age_min, age_max=age_max))
    if str(finded_user) == '[]':
        finded_user = search_person(x_left=y_down, x_right=y_up, y_up=x_right, y_down=x_left,
                                    search_sex=search_sex, lust_id=0, age_min=age_min, age_max=age_max)
        update_db(table='couples', name='lust_couple_id', data=0, id_data=user_id)
    else:
        update_db(table='couples', name='lust_couple_id', data=finded_user[0][0], id_data=user_id)
    # Окончательная проверка
    if str(finded_user) == '[]':
        return False, False, False
    else:
        finded_user_id = finded_user[0][1]
        photo_id = finded_user[0][2]

        text = create_text(int(finded_user_id), premium_finder=user_data[4])
    return finded_user_id, text, photo_id


# Profile menu
@dp.message_handler(commands=['love'], state='*')
@dp.message_handler(Text(equals='👩‍❤️‍👨 Найти пару', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    couple_data = read_by_name(name='adv', id_data=message.from_user.id, table='couples')[0][0]
    serch_settings = read_by_name(name='adv_number', id_data=1, id_name='id', table='constants')[0][0]
    # Check when show adv
    if int(couple_data) >= int(serch_settings):
        await message.answer('Рекламный пост')
        update_db(table='couples', name='adv', data=0, id_data=message.from_user.id)
        return
    update_db(table='couples', name='adv', data=int(couple_data)+1, id_data=message.from_user.id)
    finded_user_id, text, photo_id = find_person(message.from_user.id)
    if not finded_user_id:
        await message.answer('🤷‍♂️ Мы никого не нашли, увеличьте расстояние - /settings')
        return
    await message.answer_photo(caption=text, photo=photo_id, reply_markup=user_couples_kb(user_id=message.from_user.id),
                               parse_mode='html')


# Profile menu
@dp.callback_query_handler(state=UserProfile.name, text='close_it')
async def start_menu(call: types.CallbackQuery):
    # Send main profile text
    pass
