from aiogram import types

from modules.functions.work_with_geo import adres_from_adres
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.sql_func import insert_in_db, update_db, read_by_name, read_all_2, join_sender_sex, join_sender_age, \
    search_persons_for_sender
from modules.dispatcher import Admin, AdminSender
from modules.dispatcher import bot
from modules.keyboards import without_media, confirm, sender_kb, choose_users


# Рассылка  Первый экран
@dp.callback_query_handler(text='back', state=AdminSender.choose_users)
@dp.callback_query_handler(text='admin_sender', state=Admin.start)
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Отправьте мне сюда текст сообщения')
    await AdminSender.new_text_post.set()


# Рассылка Получаем фото либо пропускаем
@dp.message_handler(state=AdminSender.new_text_post)
async def start_menu(message: types.Message):
    # проверяем есть ли запись
    sender_data = read_by_name(table='constants', id_data=message.from_user.id)
    if str(sender_data) == '[]':
        insert_in_db(table='constants', name='text', data=message.text, tg_id=message.from_user.id)
    else:
        update_db(table='constants', name='text', data=message.text, id_data=message.from_user.id)
    await message.answer(text='Отправьте мне сюда фото, видео или документ',
                         reply_markup=without_media())
    await AdminSender.new_media.set()


# Рассылка Получаем файл. Запрос на кнопки
@dp.message_handler(state=AdminSender.new_media, content_types=types.ContentType.ANY)
async def start_menu(message: types.Message):
    update_db(table='constants', name='media_type', data=message.content_type, id_data=message.from_user.id)
    if message.content_type == 'video':
        update_db(table='constants', name='media_id', data=message.video.file_id, id_data=message.from_user.id)
    elif message.content_type == 'audio':
        update_db(table='constants', name='media_id', data=message.audio.file_id, id_data=message.from_user.id)
    elif message.content_type == 'document':
        update_db(table='constants', name='media_id', data=message.document.file_id,
                  id_data=message.from_user.id)
    elif message.content_type == 'animation':
        update_db(table='constants', name='media_id', data=message.animation.file_id,
                  id_data=message.from_user.id)
    elif message.content_type == 'photo':
        update_db(table='constants', name='media_id', data=message.photo[0].file_id,
                  id_data=message.from_user.id)
    else:
        await message.answer('Ошибка типа данных, попробуйте другой файл')
        return
    await message.answer(text=f'Отправьте мне сюда до трех кнопок в таком виде:\n'
                              f'Текст кнопки\n'
                              f'URL\n'
                              f'Текст кнопки\n'
                              f'URL',
                         reply_markup=without_media())
    await AdminSender.new_k_board.set()


# Рассылка. Пропускаем ввод медиа. Запрос на клавиатуру
@dp.callback_query_handler(state=AdminSender.new_media, text='no_data')
async def start_menu(call: types.CallbackQuery):
    update_db(table='constants', name='media_type', data='text', id_data=call.from_user.id)
    await edit_text_call(call=call, text=f'Отправьте мне сюда до трех кнопок в таком виде:\n'
                                         f'Текст кнопки\n'
                                         f'URL\n'
                                         f'Текст кнопки\n'
                                         f'URL',
                         k_board=without_media())
    await AdminSender.new_k_board.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. Переход по кнопке без кнопок
@dp.callback_query_handler(state=AdminSender.new_k_board, text='no_data')
async def start_menu(call: types.CallbackQuery):
    update_db(table='constants', name='k_board', data='0', id_data=call.from_user.id)
    send_data = read_by_name(table='constants', id_data=call.from_user.id)[0]
    type_msg = send_data[3]
    text_msg = send_data[2]
    media_id = send_data[4]
    if type_msg == 'photo':
        await bot.send_photo(chat_id=call.from_user.id, photo=media_id, caption=text_msg)
    elif type_msg == 'video':
        await bot.send_video(chat_id=call.from_user.id, video=media_id, caption=text_msg)
    elif type_msg == 'audio':
        await bot.send_audio(chat_id=call.from_user.id, audio=media_id, caption=text_msg)
    elif type_msg == 'animation':
        await bot.send_animation(chat_id=call.from_user.id, animation=media_id, caption=text_msg)
    elif type_msg == 'document':
        await bot.send_document(chat_id=call.from_user.id, document=media_id, caption=text_msg)
    elif type_msg == 'text':
        await bot.send_message(chat_id=call.from_user.id, text=text_msg)
    await call.message.answer('Данное сообщение будет отправленно в таком виде. Если все правильно подтвердите.',
                              reply_markup=confirm())
    await AdminSender.choose_users.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. С кнопками Нет валидации
@dp.message_handler(state=AdminSender.new_k_board)
async def start_menu(message: types.Message):
    update_db(table='constants', name='k_board', data=message.text, id_data=message.from_user.id)
    if len(message.text.split('\n')) % 2 == 0:
        send_data = read_by_name(table='constants', id_data=message.from_user.id)[0]
        type_msg = send_data[3]
        text_msg = send_data[2]
        media_id = send_data[4]
        if type_msg == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'audio':
            await bot.send_audio(chat_id=message.from_user.id, audio=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=media_id, caption=text_msg,
                                     reply_markup=sender_kb(message.text))
        elif type_msg == 'document':
            await bot.send_document(chat_id=message.from_user.id, document=media_id, caption=text_msg,
                                    reply_markup=sender_kb(message.text))
        elif type_msg == 'text':
            await bot.send_message(chat_id=message.from_user.id, text=text_msg, reply_markup=sender_kb(message.text))
        await message.answer('Данное сообщение будет отправленно в таком виде. '
                             'Если все правильно подтвердите и перейдите к выбору типа пользователей.',
                             reply_markup=confirm())
        await AdminSender.choose_users.set()
    else:
        await message.answer('Не верно введены данные. Должно быть четное количество строк')


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.choose_users, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call,
                         text='Внимание! После выбора кому отправлять сообщение рассылку нельзя будет остановить',
                         k_board=choose_users())
    await AdminSender.confirm_sender.set()


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.confirm_sender, text='send_age')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer('Введите меньший возраст.')
    await AdminSender.sender_min_age.set()


@dp.message_handler(state=AdminSender.sender_min_age)
async def start_menu(message: types.Message):
    if message.text.isdigit() and 15 <= int(message.text) <= 117:
        update_db(table='fast_info', name='fast_1', data=message.text, id_name='tg_id', id_data=message.from_user.id)
        await message.answer('Введите больший возраст. После ввода сразу начнется рассылка')
        await AdminSender.sender_max_age.set()
    else:
        await message.answer('Должно быть число от 15 до 117')


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. С кнопками Нет валидации
@dp.message_handler(state=AdminSender.sender_max_age)
async def start_menu(message: types.Message):
    min_age = read_by_name(table='fast_info', name='fast_1', id_name='tg_id', id_data=message.from_user.id)[0][0]
    if message.text.isdigit() and 15 <= int(message.text) <= 117 and message.text > min_age:
        all_users = join_sender_age(int(min_age), int(message.text))
        await start_sending(user_id=message.from_user.id, all_users=all_users)
    else:
        await message.answer('Должно быть число от 15 до 117 и больше минимального возраста')


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.confirm_sender, text='send_city')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer('Введите название города')
    await AdminSender.sender_city.set()


@dp.message_handler(state=AdminSender.sender_city)
async def start_menu(message: types.Message):
    update_db(table='fast_info', name='fast_1', data=message.text, id_name='tg_id', id_data=message.from_user.id)
    toponym_address, latitude, longitude, full_address = adres_from_adres(message.text)
    # keep params for search
    y_up = float(longitude) + 0.0089 * int(10)
    y_down = float(longitude) - 0.0089 * int(10)
    x_right = float(latitude) + 0.015187 * int(10)
    x_left = float(latitude) - 0.015187 * int(10)

    finded_users = search_persons_for_sender(x_left=y_down, x_right=y_up, y_up=x_right, y_down=x_left)

    await message.answer(f'Я нашел такой адрес: <b>{full_address}</b>\n'
                         f'Количество человек: <b>{len(finded_users)}</b>\n\n'
                         f'Начать рассылку?', reply_markup=confirm(without_back=True), parse_mode='html')
    await AdminSender.sender_city_confirm.set()


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.sender_city_confirm, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    city = read_by_name(table='fast_info', name='fast_1', id_name='tg_id', id_data=call.from_user.id)[0][0]
    toponym_address, latitude, longitude, full_address = adres_from_adres(city)
    # keep params for search
    y_up = float(longitude) + 0.0089 * int(10)
    y_down = float(longitude) - 0.0089 * int(10)
    x_right = float(latitude) + 0.015187 * int(10)
    x_left = float(latitude) - 0.015187 * int(10)

    all_users = search_persons_for_sender(x_left=y_down, x_right=y_up, y_up=x_right, y_down=x_left)
    await start_sending(user_id=call.from_user.id, all_users=all_users)


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.confirm_sender)
async def start_menu(call: types.CallbackQuery):
    if call.data == 'send_ru':
        all_users = read_all_2(name='tg_id', id_name='status', id_data='active', id_name2='language', id_data2='ru')
    elif call.data == 'send_en':
        all_users = read_all_2(name='tg_id', id_name='status', id_data='active', id_name2='language', id_data2='en')
    elif call.data == 'send_boys':
        all_users = join_sender_sex('men')
    elif call.data == 'send_girls':
        all_users = join_sender_sex('female')
    else:
        all_users = read_by_name(name='tg_id', id_name='status', id_data='active')
    all_users_admin = read_by_name(name='tg_id', id_name='status', id_data='admin')
    await start_sending(user_id=call.from_user.id, all_users=all_users+all_users_admin)


async def start_sending(user_id: int, all_users: tuple):
    await bot.send_message(text='Начинаю рассылку', chat_id=user_id)
    send_data = read_by_name(table='constants', id_data=user_id)[0]
    text_msg = send_data[2]
    type_msg = send_data[3]
    media_id = send_data[4]
    kb_data = send_data[5]
    good = 0
    bad = 0
    for one_id in all_users:
        one_id = one_id[0]
        try:
            if type_msg == 'photo':
                if kb_data == '0':
                    await bot.send_photo(chat_id=one_id, photo=media_id, caption=text_msg)
                else:
                    await bot.send_photo(chat_id=one_id, photo=media_id, caption=text_msg,
                                         reply_markup=sender_kb(kb_data))
            elif type_msg == 'video':
                if kb_data == '0':
                    await bot.send_video(chat_id=one_id, video=media_id, caption=text_msg)
                else:
                    await bot.send_video(chat_id=one_id, video=media_id, caption=text_msg,
                                         reply_markup=sender_kb(kb_data))
            elif type_msg == 'audio':
                if kb_data == '0':
                    await bot.send_audio(chat_id=one_id, audio=media_id, caption=text_msg)
                else:
                    await bot.send_audio(chat_id=one_id, audio=media_id, caption=text_msg,
                                         reply_markup=sender_kb(kb_data))
            elif type_msg == 'animation':
                if kb_data == '0':
                    await bot.send_animation(chat_id=one_id, animation=media_id, caption=text_msg)
                else:
                    await bot.send_animation(chat_id=one_id, animation=media_id, caption=text_msg,
                                             reply_markup=sender_kb(kb_data))
            elif type_msg == 'document':
                if kb_data == '0':
                    await bot.send_document(chat_id=one_id, document=media_id, caption=text_msg)
                else:
                    await bot.send_document(chat_id=one_id, document=media_id, caption=text_msg,
                                            reply_markup=sender_kb(kb_data))
            elif type_msg == 'text':
                if kb_data == '0':
                    await bot.send_message(chat_id=one_id, text=text_msg)
                else:
                    await bot.send_message(chat_id=one_id, text=text_msg, reply_markup=sender_kb(kb_data))
            good += 1
        except Exception as _ex:
            update_db(table="all_users", name="status", data="close", id_data=one_id)
            bad += 1
    await bot.send_message(text=f'Закончил рассылку\n'
                                f'успешно: {good}\n'
                                f'неудачно: {bad}', chat_id=user_id)
