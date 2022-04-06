from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging
from modules.sql_func import join_help_all, read_by_name, all_users_table
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin, User
from modules.keyboards import start_user_kb, start_admin_kb, main_user_kb


def create_help_text(tg_ig: int):
    status = False
    user_data = join_help_all(id_data=tg_ig)
    print(user_data)
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
    return status, text


# Start menu
@dp.message_handler(Text(equals='📌 Помощь', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных
    create_help_text(message.from_user.id)
    await message.answer(text='🇷🇺 Выберите язык:\n'
                              '🇺🇸 Select a language:', reply_markup=start_user_kb())
