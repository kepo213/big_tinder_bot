from aiogram import types
from main import dp
from modules.handlers.handlers_func import edit_text_call
import logging
from modules.dispatcher import bot
from modules.sql_func import update_db
from aiogram.dispatcher import FSMContext
from modules.keyboards import start_user_kb


@dp.callback_query_handler(state='*', text_contains='verifikation_')
async def start_menu(call: types.CallbackQuery):
    call_text = call.data
    await call.message.delete()
    if call_text.startswith('verifikation_close_'):
        user_id = call_text.split('verifikation_close_')[1]
        await call.message.answer("Отклонено")
        await bot.send_message(chat_id=user_id, text='Ваше фото не прошло верификацию!')
    elif call_text.startswith('verifikation_'):
        user_id = call_text.split('verifikation_')[1]
        update_db(table='fast_info', name='photo_good', data=1, id_data=user_id)
        await bot.send_message(chat_id=user_id, text='Поздравляю, вы прошли верификацию!')
        await edit_text_call(call, f"Подтверждено {user_id}")
