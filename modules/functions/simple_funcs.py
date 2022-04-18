from aiogram import types
from modules.dispatcher import bot
from modules.keyboards import start_user_kb
from modules.sql_func import insert_user, reff_user, read_by_name, update_db, grow_balls_db, chat_score_join


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
        insert_user(tg_id=message.from_user.id, name=message.from_user.first_name,
                    user_nickname=message.from_user.username)
        await message.answer(text='🇷🇺 Выберите язык:\n'
                                  '🇺🇸 Select a language:', reply_markup=start_user_kb())
    except:
        pass


async def check_balls(call: types.CallbackQuery):
    my_balls = int(read_by_name(table='fast_info', name='balls_balance', id_data=call.from_user.id)[0][0])
    if my_balls >= 100:
        update_db(table="fast_info", name="balls_balance", data=my_balls-100, id_data=call.from_user.id)
        return True
    else:
        return False


def get_right_left_btn(check_id: str, all_likes: tuple):
    index = 1
    for i in all_likes:
        if i[0] == int(check_id):
            break
        else:
            index += 1
    if index == 1:
        left = False
    else:
        left = all_likes[index-2][0]

    if index == len(all_likes):
        right = False
    else:
        right = all_likes[index][0]
    return index, left, right


def chat_roll_score(key: str):
    all_score = chat_score_join(key=key)
    if key == 'karma':
        item = 'карм'
    elif key == 'messages':
        item = 'сообщений'
    elif key == 'chats':
        item = 'диалогов'
    else:
        item = ''
    text = ''
    a = 1
    for i in all_score:
        if a == 1:
            smile = '🥇'
        elif a == 2:
            smile = '🥈'
        elif a == 3:
            smile = '🥉'
        else:
            smile = ''
        text = text + f'{smile}{a}.{i[1]}➖<b>{i[2]}</b> {item}\n'
        a += 1
    return text

