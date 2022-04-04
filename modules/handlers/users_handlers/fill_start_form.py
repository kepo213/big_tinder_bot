from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
from modules.handlers.handlers_func import edit_text_call
from modules.sql_func import insert_user, read_by_name, all_users_table, \
    update_db, create_fast_info_table, sender_table, read_all
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin, User
from aiogram.dispatcher import FSMContext
from modules.keyboards import start_user_kb, start_admin_kb, main_user_kb


@dp.callback_query_handler(state=User.start)
async def start_menu(call: types.CallbackQuery):
    call_text = call.data
    if call_text == 'ru_lang':
        pass
    elif call_text == 'en_lang':
        update_db(name='language', data='en', id_data=call.from_user.id)
    else:
        return
    await edit_text_call(call, "Добро пожаловать в наш бот знакомства! 👋\n\nВведите, пожалуйста, <b>Ваше имя!</b>")
    await User.set_name.set()


@dp.message_handler(state=User.set_name)
async def start_menu(message: types.Message):
    status = True
    check_name = str(message.text.lower())
    with open('bad_words.txt', 'r') as words:
        words = str(words.read())
        words = words.split('\n')
        for word in words:
            if word in check_name:
                status = False
                break
            else:
                pass
    if status:
        update_db(name='language', data='en', id_data=message.from_user.id)
        await message.answer('🔞 Напишите <b>Ваш возраст</b>:', parse_mode='html')
        await User.set_name.set()
    else:
        await message.answer('В вашем имени есть недопустимые слова!')
