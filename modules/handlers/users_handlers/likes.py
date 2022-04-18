from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserLikes, UserCouples
from modules.handlers.users_handlers.find_couples import show_other_profile
from modules.keyboards import user_likes_kb, likes_kb, likes_in_profile_kb
from modules.sql_func import update_db, read_by_name, search_person, join_profile_all, read_all_2, \
    insert_likes_presents_db, read_all_3
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period, get_right_left_btn


# Profile menu
@dp.message_handler(commands=['like'], state='*')
@dp.message_handler(Text(equals='💖 Симпатии', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    double1 = read_all_3(name='id', id_data=message.from_user.id, id_name2='status_from', id_data2='active',
                        id_name3='status_to', id_data3='active', table='likes')
    double2 = read_all_3(name='id', id_name='from_tg_id', id_data=message.from_user.id, id_name2='status_from',
                         id_data2='active', id_name3='status_to', id_data3='active', table='likes')
    double = double1 + double2
    all_likes_from_me = read_all_2(name='id', id_name='from_tg_id', id_data=message.from_user.id,
                                   id_name2='status_from', id_data2='active', table='likes')
    all_likes_to_me = read_all_2(name='id', id_data=message.from_user.id, id_name2='status_to', id_data2='active',
                                 table='likes')
    all_send_presents = read_all_2(name='id', id_data=message.from_user.id, id_name2='status_to', id_data2='active',
                                   table='presents')
    all_receive_presents = read_all_2(name='id', id_name="from_tg_id", id_data=message.from_user.id,
                                      id_name2='status_from', id_data2='active', table='presents')
    await message.answer(f'💖 Симпатии\n\n'
                         f'Взаимные лайки <b>{len(double)}</b> раз(-а)\n'
                         f'Вы лайкнули <b>{len(all_likes_from_me)}</b> раз(-а)\n'
                         f'Вас лайкнули <b>{len(all_likes_to_me)}</b> раз(-а)\n'
                         f'Вы отправили подарок <b>{len(all_receive_presents)}</b> раз(-а)\n'
                         f'Вы получили подарок <b>{len(all_send_presents)}</b> раз(-а)\n', parse_mode='html',
                         reply_markup=user_likes_kb())
    await UserLikes.start.set()


# Profile menu
@dp.callback_query_handler(state=UserLikes.presents_from_me, text='back')
@dp.callback_query_handler(state=UserLikes.presents_for_me, text='back')
@dp.callback_query_handler(state=UserLikes.likes_for_me, text='back')
@dp.callback_query_handler(state=UserLikes.likes_frome_me, text='back')
@dp.callback_query_handler(state=UserLikes.likes_double, text='back')
@dp.callback_query_handler(state=UserLikes.start, text='back')
async def start_menu(call: types.CallbackQuery):
    double = read_all_3(name='id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                        id_name3='status_to', id_data3='active',
                        table='likes')
    all_likes_from_me = read_all_2(name='id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                                   table='likes')
    all_likes_to_me = read_all_2(name='id', id_data=call.from_user.id, id_name2='status_to', id_data2='active',
                                 table='likes')
    all_send_presents = read_all_2(name='id', id_data=call.from_user.id, id_name2='status_to', id_data2='active',
                                   table='presents')
    all_receive_presents = read_all_2(name='id', id_name="from_tg_id", id_data=call.from_user.id,
                                      id_name2='status_from', id_data2='active', table='presents')

    await edit_text_call(call=call, text=f'💖 Симпатии\n\n'
                                         f'Взаимные лайки <b>{len(double)}</b> раз(-а)\n'
                                         f'Вы лайкнули <b>{len(all_likes_from_me)}</b> раз(-а)\n'
                                         f'Вас лайкнули <b>{len(all_likes_to_me)}</b> раз(-а)\n'
                                         f'Вы отправили подарок <b>{len(all_receive_presents)}</b> раз(-а)\n'
                                         f'Вы получили подарок <b>{len(all_send_presents)}</b> раз(-а)\n',
                         k_board=user_likes_kb())
    await UserLikes.start.set()


@dp.callback_query_handler(state=UserLikes.start, text_contains='user_')
async def start_menu(call: types.CallbackQuery):
    update_db(table='fast_info', name='fast_1', data=call.data, id_data=call.from_user.id)
    if str(call.data) == 'user_you_likes':
        text = '👍 Вам понравились'
        empty_text = '😭 Увы, но вы еще не поставили ни одного лайка.'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                               table='likes')

    elif str(call.data) == 'user_likes':
        text = '👍 Вы понравились'
        empty_text = '😭 Увы, но вы еще не получили ни одного лайка:'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_to', id_data2='active',
                               table='likes')

    elif str(call.data) == 'user_double_likes':
        text = '👍 Взаимных лайков'
        empty_text = 'Увы, но у вас еще нет взаимных симпатий, ставьте лайки другим ' \
                     'пользователям и вы обязательно найдете взаимную симпатию 😇'
        one_part = read_all_3(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                              id_name3='status_to', id_data3='active', table='likes')

        second_part = read_all_3(name='tg_id', id_name='from_tg_id', id_data=call.from_user.id, id_name2='status_from',
                                 id_data2='active', id_name3='status_to', id_data3='active', table='likes')
        all_likes = one_part + second_part

    elif str(call.data) == 'user_presents_send':
        text = '🎁 Кому отправил'
        empty_text = 'Вы еще никому не отправляли 🎁 подарки.'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name='tg_id', id_name2='status_from',
                               id_data2='active', table='presents')

    elif str(call.data) == 'user_presents_from':
        text = '🎁 От кого получил'
        empty_text = '😔 Увы, но вы еще не получили ни одно 🎁 подарка'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id,
                               id_name2='status_to', id_data2='active', table='presents')

    else:
        all_likes = '[]'
        empty_text = 'Error'
        text = 'Empty'

    if str(all_likes) == '[]':
        return await call.message.answer(empty_text)

    await edit_text_call(text=text, call=call, k_board=likes_kb(all_likes))
    await UserLikes.likes_frome_me.set()


@dp.callback_query_handler(state=UserLikes.likes_frome_me, text_contains='like_kb_delete_')
async def start_menu(call: types.CallbackQuery):

    user_id = call.data.split('_')[3]

    check_data = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    if str(check_data) == 'user_you_likes':
        pre_text = '👍 Вам понравились'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                               table='likes')
        update_db(table='likes', name='status_from', data='delete', id_data=call.from_user.id, id_name='from_tg_id')

    elif str(check_data) == 'user_likes':
        pre_text = '👍 Вы понравились'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_to', id_data2='active',
                               table='likes')
        update_db(table='likes', name='status_to', data='delete', id_data=call.from_user.id, id_name='from_tg_id')

    elif str(check_data) == 'user_double_likes':
        pre_text = '👍 Взаимных лайков'
        one_part = read_all_3(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                              id_name3='status_to', id_data3='active', table='likes')

        second_part = read_all_3(name='tg_id', id_name='from_tg_id', id_data=call.from_user.id, id_name2='status_from',
                                 id_data2='active', id_name3='status_to', id_data3='active', table='likes')
        try:
            update_db(table='likes', name='status_from', data='delete', id_data=call.from_user.id, id_name='from_tg_id')
        except:
            update_db(table='likes', name='status', data='delete', id_data=call.from_user.id, id_name='tg_id')
        all_likes = one_part + second_part

    elif str(check_data) == 'user_presents_send':
        pre_text = '🎁 Кому отправил'
        all_likes = read_all_2(name='tg_id', id_data=call.from_user.id, id_name='from_tg_id', id_name2='status_from',
                               id_data2='active', table='presents')
        update_db(table='presents', name='status_from', data='delete', id_data=call.from_user.id, id_name='tg_id')

    elif str(check_data) == 'user_presents_from':
        pre_text = '🎁 От кого получил'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id,
                               id_name2='status_to', id_data2='active', table='presents')
        update_db(table='presents', name='status_to', data='delete', id_data=call.from_user.id, id_name='from_tg_id')

    else:
        all_likes = '[]'
        pre_text = 'Empty'

    index, left, right = get_right_left_btn(check_id=user_id, all_likes=all_likes)


    all_likes = read_all_2(name='tg_id', id_data=call.from_user.id, id_name='from_tg_id', id_name2='status_from',
                           id_data2='active',
                           table='likes')
    await call.message.delete()
    if str(all_likes) == '[]':
        return await call.message.answer('😭 Увы, но вы еще не поставили ни одного лайка.')

    if left:
        user_id = right

    elif right:
        user_id = right
    else:
        return await call.message.answer('😭 Увы, но вы еще не поставили ни одного лайка.')

    index, left, right = get_right_left_btn(check_id=user_id, all_likes=all_likes)

    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)

    text = f'👍 Вам понравились <b>[{index}/{len(all_likes)}]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb(left=left, right=right, this_=user_id))
    await UserLikes.likes_frome_me.set()


@dp.callback_query_handler(state=UserLikes.likes_frome_me, text_contains='like_kb_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]

    if str(user_id) == 'stop':
        return await bot.answer_inline_query(call.id)

    check_data = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    if str(check_data) == 'user_you_likes':
        pre_text = '👍 Вам понравились'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                               table='likes')

    elif str(check_data) == 'user_likes':
        pre_text = '👍 Вы понравились'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id, id_name2='status_to', id_data2='active',
                               table='likes')

    elif str(check_data) == 'user_double_likes':
        pre_text = '👍 Взаимных лайков'
        one_part = read_all_3(name='from_tg_id', id_data=call.from_user.id, id_name2='status_from', id_data2='active',
                              id_name3='status_to', id_data3='active', table='likes')

        second_part = read_all_3(name='tg_id', id_name='from_tg_id', id_data=call.from_user.id, id_name2='status_from',
                                 id_data2='active', id_name3='status_to', id_data3='active', table='likes')
        all_likes = one_part + second_part

    elif str(check_data) == 'user_presents_send':
        pre_text = '🎁 Кому отправил'
        all_likes = read_all_2(name='tg_id', id_data=call.from_user.id, id_name='from_tg_id', id_name2='status_from',
                               id_data2='active', table='presents')

    elif str(check_data) == 'user_presents_from':
        pre_text = '🎁 От кого получил'
        all_likes = read_all_2(name='from_tg_id', id_data=call.from_user.id,
                               id_name2='status_to', id_data2='active', table='presents')

    else:
        all_likes = '[]'
        pre_text = 'Empty'

    index, left, right = get_right_left_btn(check_id=user_id, all_likes=all_likes)

    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)
    await call.message.delete()
    text = f'{pre_text} <b>[{index}/{len(all_likes)}]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb(left=left, right=right, this_=user_id))
    await UserLikes.likes_frome_me.set()
