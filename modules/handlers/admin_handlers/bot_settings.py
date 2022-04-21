import os

import emoji
from aiogram import types

from modules.functions.check_photo import search_face
from modules.functions.simple_funcs import update_age_period
from modules.functions.work_with_geo import adres_from_adres, cords_to_address
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.handlers.users_handlers.my_profile import send_main_text
from modules.keyboards import admins_settings_kb, close_it, confirm, user_couples_adv_kb, admins_settings_adv_only, \
    admins_settings_adv_chat, remove_adv, admins_fake_people, admin_bots, user_sex_kb, get_geo, get_photo, zodiac_kb
from modules.sql_func import count_all, update_adv_db, read_by_name, update_db, read_all_2, new_adv, read_adv, \
    delete_line_in_table, read_all, read_all_order, insert_first, insert_user, update_city_db
from modules.dispatcher import bot, Admin, AdminSettings


# Main settings menu
@dp.callback_query_handler(state=AdminSettings.fake_people, text='back')
@dp.callback_query_handler(state=AdminSettings.chat_roll_adv, text='back')
@dp.callback_query_handler(state=AdminSettings.adv_start, text='back')
@dp.callback_query_handler(state=Admin.start, text='admin_adv_setings')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='⚙️Выберите что хотите поменять', k_board=admins_settings_kb())
    await AdminSettings.start.set()


@dp.callback_query_handler(state=AdminSettings.adv_confirm, text='back')
@dp.callback_query_handler(state=AdminSettings.adv_photo, text='close_it')
@dp.callback_query_handler(state=AdminSettings.adv_url, text='close_it')
@dp.callback_query_handler(state=AdminSettings.adv_text, text='close_it')
@dp.callback_query_handler(state=AdminSettings.adv_number, text='close_it')
@dp.callback_query_handler(state=AdminSettings.start, text='admin_setings_adv_couples')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text=f'📺Реклама в "Найди пару"',
                         k_board=admins_settings_adv_only())
    await AdminSettings.adv_start.set()


@dp.callback_query_handler(state=AdminSettings.adv_start, text='admin_setings_adv_number')
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
@dp.callback_query_handler(state=AdminSettings.adv_start, text='admin_setings_adv_m')
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
@dp.callback_query_handler(state=AdminSettings.adv_start, text='admin_setings_adv_f')
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


# _________
# AD settings in chat_roll
@dp.callback_query_handler(state=AdminSettings.chat_roll_add_adv, text='close_it')
@dp.callback_query_handler(state=AdminSettings.start, text='admin_setings_adv_chat_roll')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📺Реклама в "Чат рулетке"',
                         k_board=admins_settings_adv_chat())
    await AdminSettings.chat_roll_adv.set()


@dp.callback_query_handler(state=AdminSettings.chat_roll_adv, text='admin_setings_chat_adv_off')
@dp.callback_query_handler(state=AdminSettings.chat_roll_adv, text='admin_setings_chat_adv_on')
async def start_menu(call: types.CallbackQuery):
    if call.data == 'admin_setings_chat_adv_off':
        update_db(table='constants', name='chat_roll_adv', data=0, id_name='id', id_data=1)
        await call.answer('Отключил ❌')
    else:
        update_db(table='constants', name='chat_roll_adv', data=1, id_name='id', id_data=1)
        await call.answer('Включил ✅')
    await edit_text_call(call=call, text='📺Реклама в "Чат рулетке"',
                         k_board=admins_settings_adv_chat())
    await AdminSettings.chat_roll_adv.set()


# Adv for MANS
@dp.callback_query_handler(state=AdminSettings.chat_roll_adv, text='admin_setings_adv_m')
async def start_menu(call: types.CallbackQuery):
    adv = read_adv(table='chat_adv', name='id, text', id_name='users_sex', id_data='men')
    if str(adv) == '[]':
        await call.message.edit_text('Рекламных постов пока что нет!')
    else:
        await call.message.edit_text('Вот последних 10 Рекламных постов. Нажмите если хотите удалить',
                                     reply_markup=remove_adv(adv))

    update_db(table="fast_info", name="fast_1", data='men', id_data=call.from_user.id)
    await call.message.answer(text=f'⚙️Настройка рекламы для чат рулетки\nОтправь мне текст рекламного поста для '
                                   f'<b>парней!</b>', reply_markup=close_it(), parse_mode='html')
    await AdminSettings.chat_roll_add_adv.set()


# Adv for FEMALES
@dp.callback_query_handler(state=AdminSettings.chat_roll_adv, text='admin_setings_adv_f')
async def start_menu(call: types.CallbackQuery):
    adv = read_adv(table='chat_adv', name='id, text', id_name='users_sex',
                   id_data='female')
    if str(adv) == '[]':
        await call.message.edit_text('Рекламных постов пока что нет!')
    else:
        await call.message.edit_text('Вот последних 10 Рекламных постов. Нажмите если хотите удалить',
                                     reply_markup=remove_adv(adv))

    update_db(table="fast_info", name="fast_1", data='female', id_data=call.from_user.id)
    await call.message.answer(text=f'⚙️Настройка рекламы\n'
                                   f'Отправь мне текст рекламного поста для <b>девушек!</b>',
                              reply_markup=close_it(), parse_mode='html')
    await AdminSettings.chat_roll_add_adv.set()


# Adv for FEMALES
@dp.callback_query_handler(state=AdminSettings.chat_roll_add_adv, text_contains='delete_ad_')
async def start_menu(call: types.CallbackQuery):
    adv_id = call.data.split('delete_ad_')[1]
    delete_line_in_table(data=adv_id)
    await call.message.answer(text='📺Реклама в "Чат рулетке"',
                              reply_markup=admins_settings_adv_chat())
    await AdminSettings.chat_roll_adv.set()


# Adv. Receive ad photo
@dp.message_handler(state=AdminSettings.chat_roll_add_adv)
async def start_menu(message: types.Message):
    sex = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    new_adv(sex=sex, text=message.text)
    await message.answer('Реклама добавлена')
    await message.answer(text='📺Реклама в "Чат рулетке"', reply_markup=admins_settings_adv_chat())
    await AdminSettings.chat_roll_adv.set()


# _________
# Work with bots
@dp.callback_query_handler(state=AdminSettings.create_bot, text='back')
@dp.callback_query_handler(state=AdminSettings.start, text='admin_settings_fake_people')
async def fake_people_start(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🌠Настройка Фэйковых анкет',
                         k_board=admins_fake_people())
    await AdminSettings.fake_people.set()


# Create new bot
@dp.callback_query_handler(state=AdminSettings.fake_people, text='new_bot')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🤖🙍 Новый бот\n'
                                         'Вы уверены что хотите создать нового бота?',
                         k_board=confirm())
    await AdminSettings.create_bot.set()


# Create new bot
@dp.callback_query_handler(state=AdminSettings.create_bot, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    bots = read_all_order(table='bots')
    if str(bots) == '[]':
        new_id = 1001
    else:
        new_id = int(bots[0][1]) + 2
    insert_first(table='bots', name='tg_id', data=new_id)
    insert_user(name='Anna', tg_id=f"{new_id}", user_nickname='0')
    update_db(table="all_users", name="status", data="bot", id_data=new_id)
    update_db(table="fast_info", name="search_range", data=0, id_data=new_id)
    await edit_text_call(call=call, text=f'🤖🙍 Новый бот\n'
                                         f'Отлично вы создали нового бота c id <b>{new_id}</b>\n'
                                         f'Для настройки перейдите в\n🤖🙍🏻‍♀️ Боты Просмотр 🙎‍♂️')
    await call.message.answer(text='🌠Настройка Фэйковых анкет', reply_markup=admins_fake_people())
    await AdminSettings.fake_people.set()


# Create new bot
@dp.callback_query_handler(state=AdminSettings.fake_people, text='admin_bot_work')
async def start_menu(call: types.CallbackQuery):
    bots = read_all_order(table='bots')
    await edit_text_call(call=call, text='🤖🙍🏻‍♀️ Боты Просмотр и редактирование 🙎‍♂️')
    if str(bots) == '[]':
        await call.message.answer('🤖 У вас еще нет ботов.')
    else:
        await call.message.answer('🤖 Вот ваши боты!', reply_markup=admin_bots(bots))
    await AdminSettings.work_with_bot.set()


# Create new bot
@dp.callback_query_handler(state=AdminSettings.work_with_bot, text_contains='admin_bot_')
async def start_menu(call: types.CallbackQuery):
    bot_id = int(call.data.split('_')[2])
    update_db(table='fast_info', name='fast_1', data=bot_id, id_data=call.from_user.id)
    await edit_text_call(call=call, text='🤖🙍🏻‍♀️ Боты Просмотр и редактирование 🙎‍♂️')
    await send_main_text(user_id=bot_id, chat_id=call.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile Name menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_name')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='👤 Напишите <b>Ваше имя:</b>', k_board=close_it())
    await AdminSettings.name.set()


# Profile NAME menu
@dp.message_handler(state=AdminSettings.name)
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
    if not status:
        await message.answer('В вашем имени имеются неприемлемые слова!')
        return
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    update_db(name='user_name', data=message.text, id_data=bot_id)
    await message.answer('Ваше имя добавлено!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile AGE menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_age')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🔞 Напишите <b>Ваш возраст:</b>', k_board=close_it())
    await AdminSettings.age.set()


# Profile AGE menu
@dp.message_handler(state=AdminSettings.age)
async def start_menu(message: types.Message):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    if message.text.isdigit():
        user_age = int(message.text)
        if user_age < 16:
            await message.answer('Минимальный возраст 16 лет')
        elif user_age > 119:
            await message.answer('В Японии самый старый человек мира Кане Танака отпраздновала 119-летие.\n'
                                 'Ты не можешь быть таким старым!')
        else:
            update_age_period(age=user_age, tg_ig=bot_id)
            update_db(table='fast_info', name='user_age', data=user_age, id_data=bot_id)
            await message.answer('Ваш возраст добавлен!')
    else:
        await message.answer('Возраст должен быть только числом')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile SEX menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_sex')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🚻 Выберите <b>Ваш пол:</b>', k_board=user_sex_kb())
    await AdminSettings.sex.set()


# Profile SEX menu
@dp.message_handler(state=AdminSettings.sex)
async def start_menu(message: types.Message):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    if message.text.lower() == 'парень':
        update_db(table='fast_info', name='user_sex', data='men', id_data=bot_id)
        update_db(table='fast_info', name='search_sex', data='female', id_data=bot_id)
    elif message.text.lower() == 'девушка':
        update_db(table='fast_info', name='user_sex', data='female', id_data=bot_id)
        update_db(table='fast_info', name='search_sex', data='men', id_data=bot_id)
    else:
        await message.answer('Нажми на кнопку ниже!', reply_markup=user_sex_kb())
        return
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile CITY menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_city')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Напишите <b>Ваш город:</b>\n'
                                         'Для точного определения местоположения, нажмите кнопку ниже!',
                         k_board=get_geo())
    await AdminSettings.city.set()


# Profile CITY menu
@dp.message_handler(state=AdminSettings.city)
async def start_menu(message: types.Message):
    try:
        city, latitude, longitude, full_adress = adres_from_adres(message.text)
        if city == 'Error' or city is None:
            await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
            return
        else:
            await message.answer(f'Я нашел такой адрес:\n'
                                 f'<b>{full_adress}</b>\n'
                                 f'Если все правильно то подтвердите.', reply_markup=confirm(without_back=True),
                                 parse_mode='html')
            bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
            update_city_db(data=city, latitude=latitude, longitude=longitude, id_data=bot_id)
    except:
        return
    await AdminSettings.city.set()


# Profile CITY menu
@dp.message_handler(content_types=['location'], state=AdminSettings.city)
async def fill_form(message: types.Message):
    x = message.location.latitude
    y = message.location.longitude
    address = cords_to_address(x=x, y=y)
    if address == 'Error':
        await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
        return
    address, latitude, longitude, full_adress = adres_from_adres(address)
    if address == 'Error':
        await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
        return
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    update_city_db(data=address, latitude=latitude, longitude=longitude, id_data=bot_id)
    await message.answer('Ваш город изменен!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile CITY menu
@dp.callback_query_handler(state=AdminSettings.city, text='yes_all_good')
async def fill_form(call: types.CallbackQuery):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    await call.message.answer('Ваш город изменен!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=call.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile PHOTO menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_photo')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📷 Пришлите <b>Ваше фото</b> или установите фото из профиля Telegram.\n\n'
                                         'Если в вашем профиле нет фотографий или они скрыты настройками приватности, '
                                         'то фотография не загрузится и лучше загрузите ваше фото в ручную.')
    await AdminSettings.photo.set()


# Profile PHOTO menu
@dp.message_handler(state=AdminSettings.photo, content_types=types.ContentTypes.PHOTO)
async def fill_form(message: types.Message):
    try:
        file_name = f"{str(message.from_user.id)}.jpg"
        await message.photo[-1].download(destination_file=f'modules/functions/{file_name}')
        faces_number = search_face(file_name=file_name)
        if faces_number > 0:
            bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
            update_db(table='fast_info', name='photo_id', data=message.photo[-1].file_id, id_data=bot_id)
            await message.answer('Ваша фотография добавлена!', reply_markup=types.ReplyKeyboardRemove())
            # Send main profile text
            await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
            await AdminSettings.change_bot.set()
        else:
            await message.answer('Во время проверки вашего фото мы обнаружили подозрительный контент!\n'
                                 'Возможные причины:\n'
                                 '- на фото нет лица или не обнаружено реального человека;\n'
                                 '- высокий процент наготы;\n'
                                 '- на фото более одного человека;')
        os.remove(f'modules/functions/{file_name}')
    except:
        pass


# Profile PHOTO menu
@dp.message_handler(state=AdminSettings.photo)
async def fill_form(message: types.Message):
    await message.answer('Я жду от тебя фото.')


# Profile ABOUT menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_about')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📝 Расскажите о себе:\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await AdminSettings.about.set()


# Profile ABOUT menu
@dp.message_handler(state=AdminSettings.about)
async def start_menu(message: types.Message):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    update_db(table='fast_info', name='about_text', data=message.text, id_data=bot_id)
    await message.answer('Добавлено!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile EMOJI menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_emoji')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Отправьте эмодзи, который хотите поставить перед своим именем!\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await AdminSettings.emoji.set()


# Profile EMOJI menu
@dp.message_handler(state=AdminSettings.emoji)
async def start_menu(message: types.Message):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]

    if emoji.demojize(message.text).startswith(':') and emoji.demojize(message.text).endswith(':'):
        update_db(table='fast_info', name='emoji', data=message.text, id_data=bot_id)
        await message.answer('Добавлено!')
        # Send main profile text
        await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
        await AdminSettings.change_bot.set()
    elif message.text == '0':
        update_db(table='fast_info', name='emoji', data=message.text, id_data=bot_id)
        await message.answer('Удалено!')
        # Send main profile text
        await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
        await AdminSettings.change_bot.set()
    else:
        await message.answer('Нельзя добавлять текст! Пришлите пожалуйста emoji!')


# Profile ZODIAC menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_zodiac')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer(text='Выберите ваш знак:', reply_markup=zodiac_kb())
    await AdminSettings.zodiac.set()


# Profile ZODIAC menu
@dp.callback_query_handler(state=AdminSettings.zodiac, text_contains='zodiac_')
async def start_menu(call: types.CallbackQuery):
    if call.data == 'zodiac_aries':
        zodiac = '♈️ Овен'
    elif call.data == 'zodiac_taurus':
        zodiac = '♉️ Телец'
    elif call.data == 'zodiac_gemini':
        zodiac = '♊️ Близнецы'

    elif call.data == 'zodiac_cancer':
        zodiac = '♋️ Рак'
    elif call.data == 'zodiac_leo':
        zodiac = '♌️ Лев'
    elif call.data == 'zodiac_virgo':
        zodiac = '♍️ Дева'

    elif call.data == 'zodiac_libra':
        zodiac = '♎️ Весы'
    elif call.data == 'zodiac_scorpio':
        zodiac = '♏️ Скорпион'
    elif call.data == 'zodiac_sagittarius':
        zodiac = '♐️ Стрелец'

    elif call.data == 'zodiac_capricorn':
        zodiac = '♑️ Козерог'
    elif call.data == 'zodiac_aquarius':
        zodiac = '♒️ Водолей'
    elif call.data == 'zodiac_pisces':
        zodiac = '♓️ Рыбы'

    elif call.data == 'clear':
        zodiac = '0'
    else:
        return
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    update_db(table='fast_info', name='zodiac', data=zodiac, id_data=bot_id)
    await call.message.answer('Добавлено!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=call.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile INSTAGRAM menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_insta')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Пришлите ваш никнейм в Instagram\n'
                                         'Пример: <b>durov</b>\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await AdminSettings.Instagram.set()


# Profile INSTAGRAM menu
@dp.message_handler(state=AdminSettings.Instagram)
async def start_menu(message: types.Message):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=message.from_user.id)[0][0]
    update_db(table='fast_info', name='instagram', data=message.text, id_data=bot_id)
    if message.text == '0':
        await message.answer('Ваш инстаграм удален!')
    else:
        await message.answer('Ваш инстаграм добавлен!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=message.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile Close/Open profile menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_close')
async def start_menu(call: types.CallbackQuery):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    status = read_by_name(table='fast_info', name='search_status', id_data=bot_id)[0][0]
    if status == 0:
        update_db(table='fast_info', name='search_status', data=1, id_data=bot_id)
        await edit_text_call(call=call, text='🙋Вы показали свою анкету в поиске!')
    else:
        update_db(table='fast_info', name='search_status', data=0, id_data=bot_id)
        await edit_text_call(call=call, text='🙅Вы скрыли свою анкету в поиске!')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=call.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile Close/Open profile menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='profile_good')
async def start_menu(call: types.CallbackQuery):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    status = read_by_name(table='fast_info', name='photo_good', id_data=bot_id)[0][0]
    if status == "0":
        update_db(table='fast_info', name='photo_good', data=1, id_data=bot_id)
        await edit_text_call(call=call, text='🙋 ✅ Вы подтвердили фото')
    else:
        update_db(table='fast_info', name='photo_good', data=0, id_data=bot_id)
        await edit_text_call(call=call, text='🙅 ❌ Отменили подтверждение фото')
    # Send main profile text
    await send_main_text(user_id=bot_id, chat_id=call.from_user.id, delete=True)
    await AdminSettings.change_bot.set()


# Profile INSTAGRAM menu
@dp.callback_query_handler(state=AdminSettings.change_bot, text='delete_bot')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='❌🤖Вы точно хотите удалить данного бота?', k_board=confirm())
    await AdminSettings.delete.set()


# Profile INSTAGRAM menu
@dp.callback_query_handler(state=AdminSettings.delete, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    bot_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    delete_line_in_table(table='presents', name='tg_id', data=bot_id)
    delete_line_in_table(table='likes', name='tg_id', data=bot_id)

    delete_line_in_table(table='fast_info', name='tg_id', data=bot_id)
    delete_line_in_table(table='couples', name='tg_id', data=bot_id)
    delete_line_in_table(table='chat_roll', name='tg_id', data=bot_id)
    delete_line_in_table(table='all_users', name='tg_id', data=bot_id)
    delete_line_in_table(table='bots', name='tg_id', data=bot_id)
    await fake_people_start(call)


# Create new bot
@dp.callback_query_handler(state=AdminSettings.fake_people, text='admin_bot_off')
@dp.callback_query_handler(state=AdminSettings.fake_people, text='admin_bot_on')
async def start_menu(call: types.CallbackQuery):
    status = int(read_by_name(table='constants', name='fake_post', id_name='id', id_data=1)[0][0])
    if status == 0:
        update_db(table='constants', name='fake_post', data=1, id_name='id', id_data=1)
    else:
        update_db(table='constants', name='fake_post', data=0, id_name='id', id_data=1)
    await edit_text_call(call=call, text='🌠Настройка Фэйковых анкет',
                         k_board=admins_fake_people())
    await AdminSettings.fake_people.set()
