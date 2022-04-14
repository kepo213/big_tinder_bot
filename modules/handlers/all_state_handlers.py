from aiogram import types
from main import dp
from modules.functions.simple_funcs import check_balls
from modules.handlers.handlers_func import edit_text_call
import logging
from modules.handlers.users_handlers.find_couples import show_other_profile
from modules.dispatcher import bot
from modules.handlers.users_handlers.find_couples import find_person, show_adv
from modules.sql_func import update_db, read_by_name, insert_likes_presents_db, read_all_2
from aiogram.dispatcher import FSMContext
from modules.keyboards import user_like_like_adv_kb, user_couples_kb


@dp.callback_query_handler(state='*', text_contains='verifikation_')
async def start_menu(call: types.CallbackQuery):
    call_text = call.data
    await call.message.delete()
    if call_text.startswith('verifikation_close_'):
        user_id = call_text.split('verifikation_close_')[1]
        await call.answer("Отклонено")
        await bot.send_message(chat_id=user_id, text='Ваше фото не прошло верификацию!')
    elif call_text.startswith('verifikation_'):
        user_id = call_text.split('verifikation_')[1]
        update_db(table='fast_info', name='photo_good', data=1, id_data=user_id)
        await bot.send_message(chat_id=user_id, text='Поздравляю, вы прошли верификацию!')
        await edit_text_call(call, f"Подтверждено {user_id}")


@dp.callback_query_handler(state='*', text_contains='couple_no_adv')
@dp.callback_query_handler(state='*', text_contains='couple_no_')
async def show_next_profile(call: types.CallbackQuery):
    user_data = read_by_name(name='user_sex, balls_balance', id_data=call.from_user.id, table='fast_info')[0]
    couple_data = read_by_name(name='adv', id_data=call.from_user.id, table='couples')[0][0]
    serch_settings = read_by_name(name='adv_number', id_data=1, id_name='id', table='constants')[0][0]

    # Check when show adv
    if int(couple_data) >= int(serch_settings):
        status = await show_adv(user_sex=user_data[0], user_id=call.from_user.id)
        update_db(table='couples', name='adv', data=0, id_data=call.from_user.id)
        if status:
            return
    else:
        update_db(table='couples', name='adv', data=int(couple_data) + 1, id_data=call.from_user.id)

    finded_user_id, text, photo_id = find_person(call.from_user.id)
    if not finded_user_id:
        await call.message.answer('🤷‍♂️ Мы никого не нашли, увеличьте расстояние - /settings')
        return
    await call.message.answer_photo(caption=text, photo=photo_id, parse_mode='html',
                                    reply_markup=user_couples_kb(user_id=finded_user_id, presents=int(user_data[1])//100))


@dp.callback_query_handler(state='*', text_contains='couple_yes_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[2]
    await call.answer(text='💚 Like')
    await bot.send_message(text='Вас лайкнули показать кто?', chat_id=user_id,
                           reply_markup=user_like_like_adv_kb(call.from_user.id))
    await show_next_profile(call)


@dp.callback_query_handler(state='*', text_contains='couple_double_yes_')
async def start_menu(call: types.CallbackQuery):
    user_id = call.data.split('_')[3]
    text, photo_id = show_other_profile(user_id=int(user_id), user_finder_id=call.from_user.id)

    user_sex = read_all_2(name='id', id_name='tg_id', id_data=call.from_user.id,
                          id_name2='from_tg_id', id_data2=int(user_id), table='likes')
    if str(user_sex) == '[]':
        insert_likes_presents_db(tg_id=call.from_user.id, from_tg_id=int(user_id))
    await call.message.delete()
    await bot.send_photo(caption=text, photo=photo_id, chat_id=call.from_user.id, parse_mode='html')


@dp.callback_query_handler(state='*', text_contains='couple_double_no')
async def start_menu(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer('👎 пропустил')


@dp.callback_query_handler(state='*', text_contains='couple_present_')
async def start_menu(call: types.CallbackQuery):
    if not await check_balls(call):
        return await call.message.answer('У вас недостаточно баллов!')

    user_id = call.data.split('_')[2]
    my_user_name = read_by_name(table='all_users', name='user_name', id_data=call.from_user.id)[0][0]
    user_name = read_by_name(table='all_users', name='user_name', id_data=user_id)[0][0]
    user_nickname = read_by_name(table='fast_info', name='user_nickname', id_data=user_id)[0][0]
    insert_likes_presents_db(tg_id=int(user_id), from_tg_id=call.from_user.id, table='presents')
    if user_nickname is None:
        await call.message.answer(f'Вы получили доступ к <a href="tg://user?id={user_id}">диалогу</a> {user_name}',
                                  parse_mode='html')
    else:
        await call.message.answer(
            f'Вы получили доступ к <a href="https://t.me/{user_nickname}">диалогу</a> {user_name}', parse_mode='html')

    if call.from_user.username is None:
        await bot.send_message(text=f'К вашему диалогу купил доступ пользователь '
                                    f'<a href="tg://user?id={call.from_user.id}">{my_user_name}</a>', chat_id=user_id,
                               parse_mode='html')
    else:
        await bot.send_message(text=f'К вашему диалогу купил доступ пользователь '
                                    f'<a href="https://t.me/{call.from_user.username}">{my_user_name}</a>',
                               chat_id=user_id, parse_mode='html')
