from aiogram import types
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.keyboards import admins_settings_kb, close_it, confirm, user_couples_adv_kb
from modules.sql_func import count_all, update_adv_db, read_by_name, update_db
from modules.dispatcher import Admin, AdminSettings


# Main settings menu
@dp.callback_query_handler(state=AdminSettings.adv_confirm, text='back')
@dp.callback_query_handler(state=AdminSettings.adv_photo, text='close_it')
@dp.callback_query_handler(state=AdminSettings.adv_url, text='close_it')
@dp.callback_query_handler(state=AdminSettings.adv_text, text='close_it')
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
        await message.answer('Поменял настройки', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text='⚙️Выберите что хотите поменять', reply_markup=admins_settings_kb())
        await AdminSettings.start.set()
    else:
        await message.answer('🤦🏼‍♂️Отправь мне число!', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(state=AdminSettings.start, text='admin_settings_fake_number')
async def start_menu(call: types.CallbackQuery):
    adv_number = read_by_name(table='constants', name='fake_post', id_name='id', id_data=1)[0][0]
    await edit_text_call(call=call, text=f'⚙️Настройки частоты фэйковых анкет\n'
                                         f'Один пост фэйковой анкеты на {adv_number} анкет настоящих\n\n'
                                         f'Отправьте мне новое число',
                         k_board=close_it())
    await AdminSettings.fake_post_number.set()


@dp.message_handler(state=AdminSettings.fake_post_number)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        update_db(table="constants", name="fake_post", data=message.text, id_name='id', id_data=1)
        await message.answer('Поменял настройки', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text='⚙️Выберите что хотите поменять', reply_markup=admins_settings_kb())
        await AdminSettings.start.set()
    else:
        await message.answer('🤦🏼‍♂️Отправь мне число!', reply_markup=types.ReplyKeyboardRemove())


# Adv for MANS
@dp.callback_query_handler(state=AdminSettings.start, text='admin_setings_adv_m')
async def start_menu(call: types.CallbackQuery):
    fast_data = read_by_name(table='adv', name='users_sex, text, photo_id, btn_url', id_name='id',
                             id_data=1)[0]

    if str(fast_data[2]) == '0':
        pass
    else:
        await call.message.answer_photo(caption=fast_data[1], photo=fast_data[3], parse_mode='html',
                                        reply_markup=user_couples_adv_kb(fast_data[2]))
    update_db(table="fast_info", name="fast_1", data='men', id_data=call.from_user.id)
    await edit_text_call(call=call, text=f'⚙️Настройка рекламы\n'
                                         f'Отправь мне текст рекламного поста для <b>парней!</b>',
                         k_board=close_it())
    await AdminSettings.adv_text.set()


# Adv for FEMALES
@dp.callback_query_handler(state=AdminSettings.start, text='admin_setings_adv_f')
async def start_menu(call: types.CallbackQuery):
    fast_data = read_by_name(table='adv', name='users_sex, text, photo_id, btn_url', id_name='id',
                             id_data=2)[0]

    if str(fast_data[2]) == '0':
        pass
    else:
        await call.message.answer_photo(caption=fast_data[1], photo=fast_data[3], parse_mode='html',
                                        reply_markup=user_couples_adv_kb(fast_data[2]))
    update_db(table="fast_info", name="fast_1", data='female', id_data=call.from_user.id)
    await edit_text_call(call=call, text=f'⚙️Настройка рекламы\n'
                                         f'Отправь мне текст рекламного поста для <b>девушек!</b>',
                         k_board=close_it())
    await AdminSettings.adv_text.set()


# Adv. Receive ad main text
@dp.message_handler(state=AdminSettings.adv_text)
async def start_menu(message: types.Message):
    update_db(table="fast_info", name="fast_2", data=message.text, id_data=message.from_user.id)
    await message.answer('Отправь мне url рекламной ссылки:\n'
                         'Пример: <b>https://www.youtube.com</b>', parse_mode='html',
                         reply_markup=close_it(), disable_web_page_preview=True)
    await AdminSettings.adv_url.set()


# Adv. Receive ad url
@dp.message_handler(state=AdminSettings.adv_url)
async def start_menu(message: types.Message):
    if ' ' in message.text or '\n' in message.text:
        await message.answer('Не верный формат ссылки!\n'
                             'Пример: <b>https://www.youtube.com</b>', parse_mode='html', reply_markup=close_it(),
                             disable_web_page_preview=True)
        return
    update_db(table="fast_info", name="fast_3", data=message.text, id_data=message.from_user.id)
    await message.answer('Отправьте мне фото для рекламного поста', parse_mode='html', reply_markup=close_it())
    await AdminSettings.adv_photo.set()


# Adv. Receive ad photo
@dp.message_handler(state=AdminSettings.adv_photo, content_types=types.ContentTypes.ANY)
async def start_menu(message: types.Message):
    if message.content_type == 'photo':
        update_db(table="fast_info", name="fast_4", data=message.photo[-1].file_id, id_data=message.from_user.id)

        fast_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3, fast_4',
                                 id_data=message.from_user.id)[0]

        await message.answer_photo(caption=fast_data[1], photo=fast_data[3], parse_mode='html',
                                   reply_markup=user_couples_adv_kb(fast_data[2]))
        if str(fast_data[0]) == 'men':
            sex = 'парней'
        else:
            sex = 'девушек'
        await message.answer(f'Реклама для: <b>{sex}</b>\n'
                             f'Подтвердите публикацию. Старая реклама будет удалена',
                             reply_markup=confirm(), parse_mode='html')
        await AdminSettings.adv_confirm.set()
    else:
        await message.answer('Я жду только фото', reply_markup=close_it())


# Adv confirm
@dp.callback_query_handler(state=AdminSettings.adv_confirm, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    fast_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3, fast_4',
                             id_data=call.from_user.id)[0]
    if str(fast_data[0]) == 'men':
        update_adv_db(text=fast_data[1], photo_id=fast_data[3], btn_url=fast_data[2], id_data=1)
    else:
        update_adv_db(text=fast_data[1], photo_id=fast_data[3], btn_url=fast_data[2], id_data=2)

    await edit_text_call(call=call, text=f'🕶Реклама запущена')
    await call.message.answer(text='⚙️Выберите что хотите поменять', reply_markup=admins_settings_kb())
    await AdminSettings.start.set()
