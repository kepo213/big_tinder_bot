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
from modules.functions.simple_funcs import update_age_period, get_right_left_btn, likes_all_inform, \
    likes_one_details_inform, likes_one_delete_inform


# Profile menu
@dp.message_handler(commands=['like'], state='*')
@dp.message_handler(Text(equals='💖 Симпатии', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    double, all_likes_from_me, all_likes_to_me, all_send_presents, \
    all_receive_presents = likes_all_inform(message.from_user.id)
    await message.answer(f'💖 Симпатии\n\n'
                         f'Взаимные лайки <b>{len(double)}</b> раз(-а)\n'
                         f'Вы лайкнули <b>{len(all_likes_from_me)}</b> раз(-а)\n'
                         f'Вас лайкнули <b>{len(all_likes_to_me)}</b> раз(-а)\n'
                         f'Вы отправили подарок <b>{len(all_send_presents)}</b> раз(-а)\n'
                         f'Вы получили подарок <b>{len(all_receive_presents)}</b> раз(-а)\n', parse_mode='html',
                         reply_markup=user_likes_kb())
    await UserLikes.start.set()


# Profile menu
@dp.callback_query_handler(state=UserLikes.check_inform, text='back')
@dp.callback_query_handler(state=UserLikes.start, text='back')
async def start_menu(call: types.CallbackQuery):
    double, all_likes_from_me, all_likes_to_me, all_send_presents, \
    all_receive_presents = likes_all_inform(call.from_user.id)
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

    all_likes, empty_text, text = likes_one_details_inform(call_data=call.data, user_id=call.from_user.id)

    if str(all_likes) == '[]':
        return await call.message.answer(empty_text)

    await edit_text_call(text=text, call=call, k_board=likes_kb(all_likes))
    await UserLikes.check_inform.set()


@dp.callback_query_handler(state=UserLikes.check_inform, text_contains='like_kb_delete_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[3]

    call_data = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    likes_one_delete_inform(call_data=call_data, user_id=call.from_user.id)
    all_likes, empty_text, pre_text = likes_one_details_inform(call_data=call_data, user_id=call.from_user.id)

    await call.message.delete()
    if str(all_likes) == '[]':
        return await call.message.answer(empty_text)

    index, left, right = get_right_left_btn(check_id=user_id, all_likes=all_likes)

    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)

    text = f'{pre_text} <b>[{index}/{len(all_likes)}]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb(left=left, right=right, this_=user_id))
    await UserLikes.check_inform.set()


@dp.callback_query_handler(state=UserLikes.check_inform, text_contains='like_kb_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]

    if str(user_id) == 'stop':
        return await bot.answer_inline_query(call.id)

    call_data = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    all_likes, empty_text, pre_text = likes_one_details_inform(call_data=call_data, user_id=call.from_user.id)
    index, left, right = get_right_left_btn(check_id=user_id, all_likes=all_likes)

    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)
    await call.message.delete()
    text = f'{pre_text} <b>[{index}/{len(all_likes)}]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb(left=left, right=right, this_=user_id))
    await UserLikes.check_inform.set()
