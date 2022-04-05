from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging
from modules.sql_func import insert_user, read_by_name, all_users_table, \
    update_db, create_fast_info_table, sender_table, read_all
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin, User
from aiogram.dispatcher import FSMContext
from modules.keyboards import start_user_kb, start_admin_kb, main_user_kb


def create_help_text(tg_ig: int):
    status = False
    user_data = read_by_name(id_data=tg_ig)
    text_data = {'name': '❌',
                 'age': '❌',
                 'sity': '❌',
                 'foto': '❌'}
    if str(user_data) == '[]':
        pass
    if user_data[0][2] == '0':
        pass
    text = f'Эта команда будет доступна, после того как вы заполните в профиле следующие данные:\n' \
           f'Имя {text_data["name"]}\n' \
           f'Возраст {text_data["age"]}\n' \
           f'Город {text_data["sity"]}\n' \
           f'Фото {text_data["foto"]}\n' \
           f'/profile - Заполнить профиль'


# Start menu
@dp.message_handler(Text(equals='📌 Помощь', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных

    await message.answer(text='🇷🇺 Выберите язык:\n'
                              '🇺🇸 Select a language:', reply_markup=start_user_kb())
