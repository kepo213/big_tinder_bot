from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserLikes, UserCouples
from modules.handlers.users_handlers.find_couples import show_other_profile
from modules.keyboards import user_likes_kb, likes_kb, likes_in_profile_kb
from modules.sql_func import update_db, read_by_name, search_person, join_profile_all, read_all_2, \
    insert_likes_presents_db
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


# Profile menu
@dp.message_handler(commands=['like'], state='*')
@dp.message_handler(Text(equals='💖 Симпатии', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    all_likes = read_by_name(name='id', id_data=message.from_user.id, table='likes')
    all_send_presents = read_by_name(name='id', id_data=message.from_user.id, table='presents')
    all_receive_presents = read_by_name(name='id', id_name="from_tg_id", id_data=message.from_user.id, table='presents')

    await message.answer(f'💖 Симпатии\n\n'
                         f'Вас лайкнули <b>{len(all_likes)}</b> раз(-а)\n'
                         f'Вы отправили подарок <b>{len(all_receive_presents)}</b> раз(-а)\n'
                         f'Вы получили подарок <b>{len(all_send_presents)}</b> раз(-а)\n', parse_mode='html',
                         reply_markup=user_likes_kb())
    await UserLikes.start.set()


# Profile menu
@dp.callback_query_handler(state=UserLikes.presents_from_me, text='back')
@dp.callback_query_handler(state=UserLikes.presents_for_me, text='back')
@dp.callback_query_handler(state=UserLikes.likes_for_me, text='back')
@dp.callback_query_handler(state=UserLikes.start, text='back')
async def start_menu(call: types.CallbackQuery):
    all_likes = read_by_name(name='id', id_data=call.from_user.id, table='likes')
    all_send_presents = read_by_name(name='id', id_data=call.from_user.id, table='presents')
    all_receive_presents = read_by_name(name='id', id_name="from_tg_id", id_data=call.from_user.id, table='presents')

    await edit_text_call(call=call, text=f'💖 Симпатии\n\n'
                                         f'Вас лайкнули <b>{len(all_likes)}</b> раз(-а)\n'
                                         f'Вы отправили подарок <b>{len(all_receive_presents)}</b> раз(-а)\n'
                                         f'Вы получили подарок <b>{len(all_send_presents)}</b> раз(-а)\n',
                         k_board=user_likes_kb())
    await UserLikes.start.set()


@dp.callback_query_handler(state=UserLikes.start, text='user_likes')
async def start_menu(call: types.CallbackQuery):
    all_likes = read_by_name(name='from_tg_id', id_data=call.from_user.id, table='likes')
    update_db(table='fast_info', name='fast_1', data=str(all_likes), id_data=call.from_user.id)
    if str(all_likes) == '[]':
        return await call.message.answer('Увы, но у вас еще нет взаимных симпатий, ставьте лайки другим '
                                         'пользователям и вы обязательно найдете взаимную симпатию 😇')

    await edit_text_call(text='👍 Вас лайкнули', call=call, k_board=likes_kb(all_likes))
    await UserLikes.likes_for_me.set()


@dp.callback_query_handler(state=UserLikes.start, text='user_presents_send')
async def start_menu(call: types.CallbackQuery):
    all_likes = read_by_name(name='tg_id', id_name="from_tg_id", id_data=call.from_user.id, table='presents')
    update_db(table='fast_info', name='fast_1', data=str(all_likes), id_data=call.from_user.id)
    if str(all_likes) == '[]':
        return await call.message.answer('Вы еще никому не отправляли 🎁 подарки.')

    await edit_text_call(text='🎁 Кому отправил', call=call, k_board=likes_kb(all_likes))
    await UserLikes.presents_from_me.set()


@dp.callback_query_handler(state=UserLikes.start, text='user_presents_from')
async def start_menu(call: types.CallbackQuery):
    all_likes = read_by_name(name='from_tg_id', id_name="tg_id", id_data=call.from_user.id, table='presents')
    update_db(table='fast_info', name='fast_1', data=str(all_likes), id_data=call.from_user.id)
    if str(all_likes) == '[]':
        return await call.message.answer('😔 Увы, но вы еще не получили ни одно 🎁 подарка')

    await edit_text_call(text='🎁 От кого получил', call=call, k_board=likes_kb(all_likes))
    await UserLikes.presents_for_me.set()


@dp.callback_query_handler(state=UserLikes.likes_for_me, text_contains='like_kb_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]
    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)
    await call.message.delete()
    text = f'👍 Вас лайкнули <b>[1/2]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb())
    await UserLikes.likes_for_me.set()


@dp.callback_query_handler(state=UserLikes.presents_from_me, text_contains='like_kb_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]
    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)
    await call.message.delete()
    text = f'🎁 Кому отправил <b>[1/2]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb())
    await UserLikes.presents_from_me.set()


@dp.callback_query_handler(state=UserLikes.presents_for_me, text_contains='like_kb_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]
    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)
    await call.message.delete()
    text = f'🎁 От кого получил <b>[1/2]</b>\n\n{text}'
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html',
                         reply_markup=likes_in_profile_kb())
    await UserLikes.presents_for_me.set()
