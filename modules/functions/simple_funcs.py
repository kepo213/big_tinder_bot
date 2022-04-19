from aiogram import types
from modules.dispatcher import bot
from modules.keyboards import start_user_kb
from modules.sql_func import insert_user, reff_user, read_by_name, update_db, grow_balls_db, chat_score_join, \
    read_all_3, read_all_2, read_adv, get_ad_by_sex


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
        update_db(table="fast_info", name="balls_balance", data=my_balls - 100, id_data=call.from_user.id)
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
        left = all_likes[index - 2][0]

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


def likes_all_inform(user_id: int):
    double1 = read_all_3(name='id', id_data=user_id, id_name2='status_from', id_data2='active',
                         id_name3='status_to', id_data3='active', table='likes')
    double2 = read_all_3(name='id', id_name='from_tg_id', id_data=user_id, id_name2='status_from',
                         id_data2='active', id_name3='status_to', id_data3='active', table='likes')
    double = double1 + double2
    all_likes_from_me1 = read_all_2(name='id', id_name='from_tg_id', id_data=user_id,
                                    id_name2='status_from', id_data2='active', table='likes')
    all_likes_from_me2 = read_all_2(name='id', id_name='tg_id', id_data=user_id,
                                    id_name2='status_to', id_data2='active', table='likes')
    all_likes_from_me = all_likes_from_me1 + all_likes_from_me2
    all_likes_to_me_1 = read_all_2(name='id', id_name='tg_id', id_data=user_id, id_name2='status_to',
                                   id_data2='no', table='likes')
    all_likes_to_me_2 = read_all_2(name='id', id_name='tg_id', id_data=user_id, id_name2='status_to',
                                   id_data2='active', table='likes')
    all_likes_to_me_3 = read_all_2(name='id', id_name='from_tg_id', id_data=user_id, id_name2='status_from',
                                   id_data2='active', table='likes')
    all_likes_to_me = all_likes_to_me_1 + all_likes_to_me_2 + all_likes_to_me_3
    all_send_presents = read_all_2(name='id', id_name="from_tg_id", id_data=user_id, id_name2='status_from',
                                   id_data2='active', table='presents')
    all_receive_presents = read_all_2(name='id', id_name="tg_id", id_data=user_id,
                                      id_name2='status_to', id_data2='no', table='presents')
    return double, all_likes_from_me, all_likes_to_me, all_send_presents, all_receive_presents


def likes_one_details_inform(call_data: str, user_id: int):
    if str(call_data) == 'user_you_likes':
        text = '👍 Вам понравились'
        empty_text = '😭 Увы, но вы еще не поставили ни одного лайка.'
        all_likes_from_me1 = read_all_2(name='tg_id', id_name='from_tg_id', id_data=user_id,
                                        id_name2='status_from', id_data2='active', table='likes')
        all_likes_from_me2 = read_all_2(name='from_tg_id', id_name='tg_id', id_data=user_id,
                                        id_name2='status_to', id_data2='active', table='likes')
        all_likes = all_likes_from_me1 + all_likes_from_me2

    elif str(call_data) == 'user_likes':
        text = '👍 Вы понравились'
        empty_text = '😭 Увы, но вы еще не получили ни одного лайка:'
        all_likes_to_me_1 = read_all_2(name='from_tg_id', id_name='tg_id', id_data=user_id, id_name2='status_to',
                                       id_data2='no', table='likes')
        all_likes_to_me_2 = read_all_2(name='from_tg_id', id_name='tg_id', id_data=user_id, id_name2='status_to',
                                       id_data2='active', table='likes')
        all_likes_to_me_3 = read_all_2(name='tg_id', id_name='from_tg_id', id_data=user_id, id_name2='status_from',
                                       id_data2='active', table='likes')
        all_likes = all_likes_to_me_1 + all_likes_to_me_2 + all_likes_to_me_3

    elif str(call_data) == 'user_double_likes':
        text = '👍 Взаимных лайков'
        empty_text = 'Увы, но у вас еще нет взаимных симпатий, ставьте лайки другим ' \
                     'пользователям и вы обязательно найдете взаимную симпатию 😇'
        double1 = read_all_3(name='from_tg_id', id_name='tg_id', id_data=user_id, id_name2='status_from',
                             id_data2='active', id_name3='status_to', id_data3='active', table='likes')
        double2 = read_all_3(name='tg_id', id_name='from_tg_id', id_data=user_id, id_name2='status_from',
                             id_data2='active', id_name3='status_to', id_data3='active', table='likes')
        all_likes = double1 + double2

    elif str(call_data) == 'user_presents_send':
        text = '🎁 Кому отправил'
        empty_text = 'Вы еще никому не отправляли 🎁 подарки.'
        all_likes = read_all_2(name='tg_id', id_name="from_tg_id", id_data=user_id, id_name2='status_from',
                               id_data2='active', table='presents')

    elif str(call_data) == 'user_presents_from':
        text = '🎁 От кого получил'
        empty_text = '😔 Увы, но вы еще не получили ни одно 🎁 подарка'
        all_likes = read_all_2(name='from_tg_id', id_name="tg_id", id_data=user_id,
                               id_name2='status_to', id_data2='no', table='presents')

    else:
        all_likes = '[]'
        empty_text = 'Error'
        text = 'Empty'
    return all_likes, empty_text, text


def likes_one_delete_inform(call_data: str, user_id: int):
    if str(call_data) == 'user_you_likes':
        all_likes_from_me = read_all_2(name='id', id_name='from_tg_id', id_data=user_id,
                                       id_name2='status_from', id_data2='active', table='likes')
        if str(all_likes_from_me) != '[]':
            update_db(table='likes', name='status_from', data='delete', id_name='from_tg_id', id_data=user_id)
        else:
            update_db(table='likes', name='status_to', data='delete', id_name='tg_id', id_data=user_id)

    elif str(call_data) == 'user_likes':

        all_likes_from_me = read_all_2(name='id', id_name='from_tg_id', id_data=user_id,
                                       id_name2='status_from', id_data2='active', table='likes')
        if str(all_likes_from_me) != '[]':
            update_db(table='likes', name='status_from', data='delete', id_name='from_tg_id', id_data=user_id)
        else:
            update_db(table='likes', name='status_to', data='delete', id_name='tg_id', id_data=user_id)

    elif str(call_data) == 'user_double_likes':
        all_likes_from_me = read_all_2(name='id', id_name='from_tg_id', id_data=user_id,
                                       id_name2='status_from', id_data2='active', table='likes')
        if str(all_likes_from_me) != '[]':
            update_db(table='likes', name='status_from', data='delete', id_name='from_tg_id', id_data=user_id)
        else:
            update_db(table='likes', name='status_to', data='delete', id_name='tg_id', id_data=user_id)

    elif str(call_data) == 'user_presents_send':
        update_db(table='presents', name='status_from', data='delete', id_name='from_tg_id', id_data=user_id)

    elif str(call_data) == 'user_presents_from':
        update_db(table='presents', name='status_to', data='delete', id_name='tg_id', id_data=user_id)

    else:
        pass


async def send_chat_roll_ad(user_id: int):
    # Check have bot any AD in database:
    user_sex = read_by_name(table='fast_info', name="user_sex", id_data=user_id)[0][0]
    lust_ad_number = read_by_name(table='chat_roll', name="lust_adv", id_name='tg_id', id_data=user_id)[0][0]
    adv = get_ad_by_sex(sex=user_sex, lust_ad_id=lust_ad_number)
    if str(adv) == '[]':
        update_db(table='chat_roll', name="lust_adv", data=0, id_data=user_id)
        adv = get_ad_by_sex(sex=user_sex, lust_ad_id=0)
        if str(adv) == '[]':
            return
        else:
            await bot.send_message(chat_id=user_id, text=adv[0][1], parse_mode='html', disable_web_page_preview=True)
    else:
        update_db(table='chat_roll', name="lust_adv", data=adv[0][0], id_data=user_id)
        await bot.send_message(chat_id=user_id, text=adv[0][1], parse_mode='html', disable_web_page_preview=True)


async def show_chat_roll_adv(user_id: int, friend_id: int):
    # Check the on/off AD in chat_roll
    show_adv = read_by_name(table='constants', name="chat_roll_adv", id_name='id', id_data=1)[0][0]
    if int(show_adv) == 0:
        return
    await send_chat_roll_ad(user_id)
    await send_chat_roll_ad(friend_id)
