from aiogram import types
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.keyboards import admins_settings_kb, close_it
from modules.sql_func import count_all, read_all_by_date, read_by_name, update_db
from modules.dispatcher import Admin, AdminSettings


@dp.callback_query_handler(state=AdminSettings.adv_number, text='close_it')
@dp.callback_query_handler(state=Admin.start, text='admin_setings')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='⚙️Выберите что хотите поменять', k_board=admins_settings_kb())
    await AdminSettings.start.set()


@dp.callback_query_handler(state=AdminSettings.start, text='admin_setings_adv_number')
async def start_menu(call: types.CallbackQuery):
    adv_number = read_by_name(table='constants', name='adv_number', id_name='id', id_data=1)[0][0]
    await edit_text_call(call=call, text=f'⚙️Настройки рекламы.\n'
                                         f'Один пост рекламы на {adv_number} анкет\n\n'
                                         f'Отправьте мне новое число',
                         k_board=close_it())
    await AdminSettings.adv_number.set()


@dp.message_handler(state=AdminSettings.adv_number)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        update_db(table="constants", name="adv_number", data=message.text, id_name='id', id_data=1)
        await message.answer('Поменял настройки')
        await message.answer(text='⚙️Выберите что хотите поменять', reply_markup=admins_settings_kb())
        await AdminSettings.start.set()
    else:
        await message.answer('🤦🏼‍♂️Отправь мне число!')
