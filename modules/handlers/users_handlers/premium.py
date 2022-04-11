import os
import emoji

from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserPremium
from modules.functions.check_photo import search_face
from modules.keyboards import reff_kb, user_profile_kb, close_it, get_geo, confirm, get_photo, zodiac_kb, \
    user_verifikation_kb
from modules.functions.work_with_geo import adres_from_adres, cords_to_address
from modules.sql_func import update_db, read_by_name, join_profile_all
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


# Profile menu
@dp.message_handler(Text(equals='💎 Премиум', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    url = f'https://t.me/test_superpuper_wdk_bot?start={message.from_user.id}'
    await message.answer('💎 Ваш баланс: <b>100</b> баллов\n\n'
                         '🎁 За отправленный подарок другому пользователю, вы сможете сразу получить доступ к '
                         'диалогу с ним.\n\n🛍 Стоимость 1-го подарка: <b>100</b> баллов\n\n'
                         '👥 За каждого приглашенного друга по реферальной ссылке вы получите <b>50</b> баллов',
                         reply_markup=reff_kb(url))


# Profile menu
@dp.callback_query_handler(state=UserPremium.start, text='close_it')
async def start_menu(call: types.CallbackQuery):
    url = f'https://t.me/test_superpuper_wdk_bot?start={call.from_user.id}'
    await call.message.answer('💎 Ваш баланс: <b>100</b> баллов\n\n'
                         '🎁 За отправленный подарок другому пользователю, вы сможете сразу получить доступ к '
                         'диалогу с ним.\n\n🛍 Стоимость 1-го подарка: <b>100</b> баллов\n\n'
                         '👥 За каждого приглашенного друга по реферальной ссылке вы получите <b>50</b> баллов',
                         reply_markup=reff_kb(url))

