from aiogram import types

from modules import dp, update_db
from modules.dispatcher import AdminAutoSender, Admin
from modules.handlers.handlers_func import edit_text_call
from modules.keyboards import smart_sender, smart_sender_post_type, without_media
from modules.sql_func import read_by_name


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
    await edit_text_call(call=call,
                         text=f'📝 Новый пост ✈️\n'
                              f'Пост отправиться спустя n дней после регистрации либо последнего входа в бот\n'
                              f'<b>Введите количество дне после которых будет отправленно сообщение</b>\n')
    await AdminAutoSender.new_post_data.set()


@dp.message_handler(state=AdminAutoSender.new_post_data)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        if 0 < int(message.text) <= 60:
            update_db(table="fast_info", name="fast_2", data=message.text, id_data=message.from_user.id)
            await message.answer(f'📝 Новый пост ✈️\nВведите текст поста')
            await AdminAutoSender.new_post_text.set()
        else:
            await message.answer('Количество дней должно быть от 0 до 60')
    else:
        await message.answer('Только цифры!')


@dp.message_handler(state=AdminAutoSender.new_post_text)
async def start_menu(message: types.Message):
    update_db(table="fast_info", name="fast_3", data=message.text, id_data=message.from_user.id)
    await message.answer(f'📝 Новый пост ✈️\nВведите данные кнопки в формате:\n'
                         f'<b>Текст кнопки</b>\n'
                         f'url', parse_mode='html', reply_markup=without_media())
    await AdminAutoSender.new_post_url.set()


@dp.message_handler(state=AdminAutoSender.new_post_url)
async def start_menu(message: types.Message):
    if '\n' in message.text:
        post_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3', id_data=message.from_user.id)
        await message.answer(f'Пост опубликован!')
        await AdminAutoSender.new_post_url.set()
    else:
        await message.answer('Не верный формат')


@dp.callback_query_handler(state=AdminAutoSender.new_post_url, text='no_data')
async def start_menu(call: types.CallbackQuery):
    post_data = read_by_name(table='fast_info', name='fast_1, fast_2, fast_3', id_data=call.from_user.id)
    await call.message.answer(reply_markup=smart_sender_post_type(),
                              text=f'Пост опубликован!')
    await AdminAutoSender.new_post_url.set()
