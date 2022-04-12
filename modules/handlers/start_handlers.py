from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging
from modules.functions.simple_funcs import start_reffs
from modules.handlers.handlers_func import edit_text_call
from modules.sql_func import insert_user, read_by_name, all_users_table, for_couples_table,\
    update_db, create_fast_info_table, sender_table, read_all, photo_table, reffs_table
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin, User, AdminSettings
from aiogram.dispatcher import FSMContext
from modules.keyboards import start_user_kb, start_admin_kb, main_user_kb


# Start menu
@dp.message_handler(commands=['start'], state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных
    user_data = read_by_name(id_data=message.from_user.id)
    if str(user_data) == '[]' and not message.text.startswith('/start reff'):
        insert_user(tg_id=message.from_user.id, name=message.from_user.first_name)
        await message.answer(text='🇷🇺 Выберите язык:\n'
                                  '🇺🇸 Select a language:', reply_markup=start_user_kb())
    elif str(user_data) == '[]' and message.text.startswith('/start reff'):
        await start_reffs(message)
    elif user_data[0][3] == 'admin':
        await message.answer('Привет админ', reply_markup=start_admin_kb())
        await Admin.start.set()
        return
    elif user_data[0][3] == 'close':
        await message.answer('🔙Главное меню', reply_markup=main_user_kb())
        update_db(table="all_users", name="status", data="active", id_data=message.from_user.id)
    elif user_data[0][3] == 'need_reg':
        insert_user(tg_id=message.from_user.id, name=message.from_user.first_name)
        await message.answer(text='Ваша регистрация не была завершена! Заполните ее заново!')
        await message.answer(text='🇷🇺 Выберите язык:\n'
                                  '🇺🇸 Select a language:', reply_markup=start_user_kb())
    else:
        await message.answer('🔙Главное меню', reply_markup=main_user_kb())
    await User.start.set()


# Start menu
@dp.callback_query_handler(state=Admin.start, text='admin_as_user')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer('🔙Главное меню', reply_markup=main_user_kb())
    await User.start.set()


# Start menu
@dp.callback_query_handler(state=AdminSettings.start, text='back')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(text='Привет админ', k_board=start_admin_kb(), call=call)
    await Admin.start.set()


# Start menu
@dp.message_handler(commands=['create_db'], state='*')
async def start_menu(message: types.Message):
    # Создаем все таблицы в бд
    create_fast_info_table()
    for_couples_table()
    all_users_table()
    sender_table()
    photo_table()
    reffs_table()
    await message.answer(text='Я создал все базы данных')


# Start menu
@dp.message_handler(commands=['i_am_admin'], state='*')
async def start_menu(message: types.Message):
    # Создаем все таблицы в бд
    update_db(name='status', data='admin', id_data=message.from_user.id)
    await message.answer(text='Ты теперь админ')


# Cancel all process
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.reply('Процес отменен. Все данные стерты. Что бы начать все с начала нажми /start',
                        reply_markup=types.ReplyKeyboardRemove())
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


# Set admin
@dp.message_handler(commands=['id'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Твой {message.from_user.id}\n'
                         f'Чат {message.chat.id}')


# Get users
@dp.message_handler(commands=['get_all_users'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Начал собирать файл')
    data = read_all()
    number, bad = upload_all_data(data)
    await message.answer(f'Успешно {number}, ошибок {bad}\n\nЗагружаю')
    with open("all_users.xlsx", 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file, caption="Все сделано!")


# Get users
@dp.message_handler(commands=['get_all_users_id'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Начал собирать файл')
    data = read_all()
    number, bad = upload_all_users_id(data)
    await message.answer(f'Успешно {number}, ошибок {bad}\n\nЗагружаю')
    with open("all_users.xlsx", 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file, caption="Все сделано!")


# # Start menu
# @dp.message_handler(state='*', content_types=types.ContentType.ANY)
# async def start_menu(message: types.Message):
#     print(message.photo[0].file_id)
#     try:
#         await message.answer(message.forward_from_chat.id)
#     except:
#         pass
