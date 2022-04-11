from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserPremium
from modules.keyboards import reff_kb, user_profile_kb, close_it, get_geo, confirm, get_photo, zodiac_kb, \
    user_verifikation_kb
from modules.functions.work_with_geo import adres_from_adres, cords_to_address
from modules.sql_func import update_db, read_by_name, join_reff_block, join_reff_premium, join_reff_photo
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


# Reff menu
@dp.message_handler(Text(equals='💎 Премиум', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    data = read_by_name(table='fast_info', name='balls_balance', id_data=message.from_user.id)[0][0]
    url = f'https://t.me/test_superpuper_wdk_bot?start=reff{message.from_user.id}'
    await message.answer(f'💎 Ваш баланс: <b>{data}</b> баллов\n\n'
                         f'🎁 За отправленный подарок другому пользователю, вы сможете сразу получить доступ к '
                         f'диалогу с ним.\n\n🛍 Стоимость 1-го подарка: <b>100</b> баллов\n\n'
                         f'👥 За каждого приглашенного друга по реферальной ссылке вы получите <b>50</b> баллов',
                         reply_markup=reff_kb(url), parse_mode='html')
    await UserPremium.start.set()


# Reff menu
@dp.callback_query_handler(state=UserPremium.start, text='back')
async def start_menu(call: types.CallbackQuery):
    data = read_by_name(table='fast_info', name='balls_balance', id_data=call.from_user.id)[0][0]
    url = f'https://t.me/test_superpuper_wdk_bot?start=reff{call.from_user.id}'
    await edit_text_call(call=call, text=f'💎 Ваш баланс: <b>{data}</b> баллов\n\n'
                                         f'🎁 За отправленный подарок другому пользователю, вы сможете сразу получить '
                                         f'доступ к диалогу с ним.\n\n🛍 Стоимость 1-го подарка: <b>100</b> баллов\n\n'
                                         f'👥 За каждого приглашенного друга по реферальной ссылке вы получите '
                                         f'<b>50</b> баллов',
                         k_board=reff_kb(url))
    await UserPremium.start.set()


# Reff menu
@dp.callback_query_handler(state=UserPremium.start, text='premium_reff')
async def start_menu(call: types.CallbackQuery):
    all_users = read_by_name(table='reff', id_name='mentor_tg_id', id_data=call.from_user.id)
    all_block = join_reff_block(tg_id=call.from_user.id)
    all_photo = join_reff_photo(tg_id=call.from_user.id)
    all_premium = join_reff_premium(tg_id=call.from_user.id)
    url = f'https://t.me/test_superpuper_wdk_bot?start=reff{call.from_user.id}'
    await edit_text_call(call=call, text=f'👥 Вы пригласили - {len(all_users)}\n'
                                         f'💎 Купили премиум - {len(all_premium)}\n'
                                         f'📷 Добавили фото - {len(all_users)-len(all_photo)}\n'
                                         f'❌ Заблокировали бот - {len(all_block)}\n\n'
                                         f'👤 Ваша реферальная ссылка: {url}',
                         k_board=reff_kb(url, True))
