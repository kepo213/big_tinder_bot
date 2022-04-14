from aiogram import types
from modules.dispatcher import bot
from modules.sql_func import update_db
from modules.keyboards import start_user_kb
from modules.sql_func import insert_user, reff_user, read_by_name, \
    update_db, grow_balls_db, sender_table, read_all, photo_table, reffs_table


def update_age_period(tg_ig: int, age: int):
    if 16 <= age <= 18:
        update_db(table='fast_info', name='age_min', data=16, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=18, id_data=tg_ig)
    elif 18 <= age <= 24:
        update_db(table='fast_info', name='age_min', data=18, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=24, id_data=tg_ig)
    elif 24 <= age <= 29:
        update_db(table='fast_info', name='age_min', data=24, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=30, id_data=tg_ig)
    elif 30 <= age <= 35:
        update_db(table='fast_info', name='age_min', data=30, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=35, id_data=tg_ig)
    elif 36 <= age <= 45:
        update_db(table='fast_info', name='age_min', data=36, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=45, id_data=tg_ig)
    elif 46 <= age <= 60:
        update_db(table='fast_info', name='age_min', data=46, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=60, id_data=tg_ig)
    elif 60 <= age <= 80:
        update_db(table='fast_info', name='age_min', data=60, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=80, id_data=tg_ig)
    elif 80 <= age <= 120:
        update_db(table='fast_info', name='age_min', data=80, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=120, id_data=tg_ig)


async def start_reffs(message: types.Message):
    try:
        reff_user_id = message.text.split('start reff')[1]
        if reff_user_id.isdigit():
            await bot.send_message(chat_id=reff_user_id,
                                   text='По вашей ссылке только что зарегистрировался новый пользователь!')
            reff_user(tg_id=message.from_user.id, mentor_tg_id=reff_user_id)
            grow_balls_db(data=reff_user_id)
        else:
            pass
        update_db(table="all_users", name="status", data="active", id_data=message.from_user.id)
        insert_user(tg_id=message.from_user.id, name=message.from_user.first_name)
        await message.answer(text='🇷🇺 Выберите язык:\n'
                                  '🇺🇸 Select a language:', reply_markup=start_user_kb())
    except:
        pass