from aiogram import types

from modules import dp, update_db
from modules.dispatcher import AdminAutoSender, Admin
from modules.handlers.handlers_func import edit_text_call
from modules.keyboards import smart_sender, smart_sender_post_type, without_media, pick_sex, show_all_posts, \
    delete_smart_sender_post, smart_sender_post_kb, confirm
from modules.sql_func import read_by_name, new_smart_sener, read_all_order, delete_line_in_table


@dp.callback_query_handler(state=AdminAutoSender.show_posts, text='back')
@dp.callback_query_handler(state=AdminAutoSender.new_post, text='back')
@dp.callback_query_handler(state=Admin.start, text='auto_sender')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📝⚙️ Авто рассылка', k_board=smart_sender())
    await AdminAutoSender.start.set()


@dp.callback_query_handler(state=AdminAutoSender.start, text='new_post')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, k_board=smart_sender_post_type(),
                         text=f'📝 Новый пост ✈️\n'
                              f'Пост отправиться спустя n дней после регистрации либо последнего входа в бот\n'
                              f'<b>Выберите когда будет отправляться рассылка.</b>\n')
    await AdminAutoSender.new_post.set()


@dp.callback_query_handler(state=AdminAutoSender.new_post, text='new_post_first_reg')
@dp.callback_query_handler(state=AdminAutoSender.new_post, text='new_post_lust_active')
async def start_menu(call: types.CallbackQuery):
    if call.data == 'new_post_first_reg':
        info = 'first_reg'
    else:
        info = 'lust_active'
    update_db(table="fast_info", name="fast_1", data=info, id_data=call.from_user.id)
    await edit_text_call(call=call, k_board=pick_sex(),
                         text=f'📝 Новый пост ✈️\n'
                              f'<b>Выберите пол</b>\n')
    await AdminAutoSender.new_post_sex.set()


@dp.callback_query_handler(state=AdminAutoSender.new_post_sex, text='for_mans')
@dp.callback_query_handler(state=AdminAutoSender.new_post_sex, text='for_females')
async def start_menu(call: types.CallbackQuery):
    if call.data == 'for_mans':
        sex = 'men'
    else:
        sex = 'female'
    update_db(table="fast_info", name="fast_2", data=sex, id_data=call.from_user.id)
    await edit_text_call(call=call,
                         text=f'📝 Новый пост ✈️\n'
                              f'Пост отправиться спустя n дней после регистрации либо последнего входа в бот\n'
                              f'<b>Введите количество дне после которых будет отправленно сообщение</b>\n')
    await AdminAutoSender.new_post_data.set()


@dp.message_handler(state=AdminAutoSender.new_post_data)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        if 0 < int(message.text) <= 60:
            update_db(table="fast_info", name="fast_3", data=message.text, id_data=message.from_user.id)
            await message.answer(f'📝 Новый пост ✈️\nВведите текст поста')
            await AdminAutoSender.new_post_text.set()
        else:
            await message.answer('Количество дней должно быть от 0 до 60')
    else:
        await message.answer('Только цифры!')


@dp.message_handler(state=AdminAutoSender.new_post_text)
async def start_menu(message: types.Message):
    update_db(table="fast_info", name="fast_4", data=message.text, id_data=message.from_user.id)
    await message.answer(f'📝 Новый пост ✈️\nОтправьте мне фото для поста\n', parse_mode='html',
                         reply_markup=without_media())
    await AdminAutoSender.new_post_photo.set()


@dp.message_handler(state=AdminAutoSender.new_post_photo, content_types=types.ContentType.PHOTO)
async def start_menu(message: types.Message):
    update_db(table="fast_info", name="fast_5", data=message.photo[-1].file_id, id_data=message.from_user.id)
    await message.answer(f'📝 Новый пост ✈️\nВведите данные кнопки в формате:\n'
                         f'<b>Текст кнопки</b>\n'
                         f'url', parse_mode='html', reply_markup=without_media())
    await AdminAutoSender.new_post_url.set()


@dp.message_handler(state=AdminAutoSender.new_post_photo)
async def start_menu(message: types.Message):
    await message.answer(f'ТОЛЬКО ФОТО')


@dp.callback_query_handler(state=AdminAutoSender.new_post_photo, text='no_data')
async def start_menu(call: types.CallbackQuery):
    update_db(table="fast_info", name="fast_5", data='0', id_data=call.from_user.id)
    await edit_text_call(text=f'📝 Новый пост ✈️\nВведите данные кнопки в формате:\n'
                              f'<b>Текст кнопки</b>\n'
                              f'url', k_board=without_media(), call=call)
    await AdminAutoSender.new_post_url.set()


@dp.message_handler(state=AdminAutoSender.new_post_url)
async def start_menu(message: types.Message):
    if '\n' in message.text:
        name = message.text.split('\n')[0]
        url = message.text.split('\n')[1]
        post_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3, fast_4, fast_5',
                                 id_data=message.from_user.id)[0]
        new_smart_sener(text=post_data[3], btn_name=name, btn_url=url, days=post_data[2], post_type=post_data[0],
                        sex=post_data[1], photo_id=post_data[4])
        await message.answer(f'Пост опубликован!')
        await message.answer(text='📝⚙️ Авто рассылка', reply_markup=smart_sender())
        await AdminAutoSender.start.set()
    else:
        await message.answer('Не верный формат')


@dp.callback_query_handler(state=AdminAutoSender.new_post_url, text='no_data')
async def start_menu(call: types.CallbackQuery):
    post_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3, fast_4, fast_5',
                             id_data=call.from_user.id)[0]
    new_smart_sener(text=post_data[3], btn_name='0', btn_url='0', days=post_data[2], post_type=post_data[0],
                    sex=post_data[1], photo_id=post_data[4])
    await edit_text_call(k_board=smart_sender_post_type(),
                         text=f'Пост опубликован!', call=call)
    await edit_text_call(call=call, text='📝⚙️ Авто рассылка', k_board=smart_sender())
    await AdminAutoSender.start.set()


@dp.callback_query_handler(state=AdminAutoSender.delete_post_confirm, text='back')
@dp.callback_query_handler(state=AdminAutoSender.delete_posts, text='back')
@dp.callback_query_handler(state=AdminAutoSender.start, text='admin_smart_sender')
async def show_all_smart_posts(call: types.CallbackQuery):
    post_data = read_all_order(table='smart_sender')
    if str(post_data) == '[]':
        await edit_text_call(call=call,
                             text=f'📝К сожелению у вас пока нет постов\n', k_board=confirm(without_yes=True))
    else:
        await edit_text_call(call=call, k_board=show_all_posts(post_data),
                             text=f'📝Вот все ваши посты\n')

    await AdminAutoSender.show_posts.set()


@dp.callback_query_handler(state=AdminAutoSender.show_posts, text_contains='smart_post_')
async def start_menu(call: types.CallbackQuery):
    post_id = int(call.data.split('_')[2])
    post_data = read_by_name(table='smart_sender', name='*', id_name='id', id_data=post_id)[0]
    update_db(table="fast_info", name="fast_1", data=post_id, id_data=call.from_user.id)
    if post_data[2] == '0':
        k_board = None
    else:
        k_board = smart_sender_post_kb(name=post_data[2], url=post_data[3])
    if post_data[7] == '0':
        await call.message.answer(text=post_data[1])

    if post_data[2] == '0':
        sex = 'Парней'
    else:
        sex = 'Девушек'

    if post_data[7] == '0':
        await call.message.answer(text=post_data[1],
                                  reply_markup=k_board, parse_mode='html')
    else:
        await call.message.answer_photo(caption=post_data[1], photo=post_data[7],
                                        reply_markup=k_board, parse_mode='html')

    await call.message.answer(f'Пост для <b>{sex}</b>\n'
                              f'Тип поста <b>{post_data[5]}</b>\n'
                              f'Количество дней <b>{post_data[4]}</b>\n',
                              reply_markup=delete_smart_sender_post(), parse_mode='html')
    await AdminAutoSender.delete_posts.set()


@dp.callback_query_handler(state=AdminAutoSender.delete_posts, text='delete_smart_sender')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, k_board=confirm(),
                         text=f'Вы точно хотите удалить данный пост?')
    await AdminAutoSender.delete_post_confirm.set()


@dp.callback_query_handler(state=AdminAutoSender.delete_post_confirm, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    post_id = read_by_name(table='fast_info', name='fast_1', id_data=call.from_user.id)[0][0]
    delete_line_in_table(table='smart_sender', name='id', data=int(post_id))
    await edit_text_call(call=call, text=f'Пост удален')

    post_data = read_all_order(table='smart_sender')
    if str(post_data) == '[]':
        await call.message.answer(text=f'📝К сожелению у вас пока нет постов\n', reply_markup=confirm(without_yes=True))
    else:
        await call.message.answer(reply_markup=show_all_posts(post_data), text=f'📝Вот все ваши посты\n')
    await AdminAutoSender.show_posts.set()
