from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text

from modules.dispatcher import UserSettings
from modules.keyboards import user_settings_kb, start_user_kb, close_it
from modules.sql_func import update_db, read_by_name
from modules.handlers.handlers_func import edit_text_call


def settings_text(user_id: int):
    user_data = read_by_name(id_data=user_id, table='fast_info', name='search_range, age_min, age_max',)
    text = f'Фильтр по подбору партнеров:\n\n' \
           f'🌐 Макс.расстояние: <b>{user_data[0][0]} км</b>\n' \
           f'🔞 Возр.диапазон: <b>{user_data[0][1]}-{user_data[0][2]} лет</b>'
    return text


# Settings menu
@dp.message_handler(commands=['settings'], state='*')
@dp.message_handler(Text(equals='⚙️ Настройка', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    await message.answer(text=settings_text(message.from_user.id), reply_markup=user_settings_kb(), parse_mode='html')
    await UserSettings.start.set()


# Settings menu
@dp.callback_query_handler(state=UserSettings.range_period, text='age_period_max')
@dp.callback_query_handler(state=UserSettings.range_period, text='age_period')
@dp.callback_query_handler(state=UserSettings.range_period, text='close_it')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text=settings_text(call.from_user.id), k_board=user_settings_kb())
    await UserSettings.start.set()


@dp.callback_query_handler(state=UserSettings.start, text='user_max_range')
async def fill_form(call: types.CallbackQuery):
    await edit_text_call(call, "Введите расстояние от вас:", k_board=close_it())
    await UserSettings.range_period.set()


@dp.message_handler(state=UserSettings.range_period)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        if int(message.text) <= 3000:
            update_db(table='fast_info', name='search_range', data=message.text, id_data=message.from_user.id)
            await message.answer('Информация о расстоянии, изменена!')
            await message.answer(text=settings_text(message.from_user.id), reply_markup=user_settings_kb(),
                                 parse_mode='html')
            await UserSettings.start.set()
        else:
            await message.answer('Максимум 3000 км')
    else:
        await message.answer('Я жду от тебя только цифры', reply_markup=close_it())


@dp.callback_query_handler(state=UserSettings.start, text='user_language')
async def fill_form(call: types.CallbackQuery):
    await edit_text_call(call, "🏳️ Язык/Language", k_board=start_user_kb())
    await UserSettings.language.set()


@dp.callback_query_handler(state=UserSettings.language, text='en_lang')
@dp.callback_query_handler(state=UserSettings.language, text='ru_lang')
async def fill_form(call: types.CallbackQuery):
    call_text = call.data
    if call_text == 'ru_lang':
        language = '🇷🇺 Русский'
        update_db(name='language', data='ru', id_data=call.from_user.id)
    elif call_text == 'en_lang':
        language = '🇺🇸 English'
        update_db(name='language', data='en', id_data=call.from_user.id)
    else:
        return

    await edit_text_call(call, f"Выбран язык: <b>{language}</b>")
    await call.message.answer(text=settings_text(call.from_user.id), reply_markup=user_settings_kb(), parse_mode='html')
    await UserSettings.start.set()


@dp.callback_query_handler(state=UserSettings.start, text='user_age_period')
async def fill_form(call: types.CallbackQuery):
    await edit_text_call(call, "Напишите минимальный возраст:", k_board=close_it())
    await UserSettings.age_period.set()


@dp.message_handler(state=UserSettings.age_period)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        if int(message.text) < 16:
            await message.answer('Минимальный возраст: 16', reply_markup=close_it())
        elif 16 <= int(message.text) <= 117:
            update_db(table='fast_info', name='fast_1', data=message.text, id_data=message.from_user.id)
            await message.answer(text='Отлично, теперь напишите максимальный возраст:', reply_markup=close_it(),
                                 parse_mode='html')
            await UserSettings.age_period_max.set()
        else:
            await message.answer('Возраст слишком большой.', reply_markup=close_it())
    else:
        await message.answer('Я жду от тебя только цифры', reply_markup=close_it())


@dp.message_handler(state=UserSettings.age_period_max)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        user_min_age = read_by_name(id_data=message.from_user.id, table='fast_info', name='fast_1')
        if int(message.text) < 16:
            await message.answer('Максимальный возраст должен быть больше: 16', reply_markup=close_it())
        elif 16 <= int(message.text) <= 117 and int(user_min_age[0][0]) < int(message.text):
            update_db(table='fast_info', name='age_min', data=user_min_age[0], id_data=message.from_user.id)
            update_db(table='fast_info', name='age_max', data=message.text, id_data=message.from_user.id)
            await message.answer(text='Отлично, диапазон настроен.')
            await message.answer(text=settings_text(message.from_user.id), reply_markup=user_settings_kb(),
                                 parse_mode='html')
            await UserSettings.start.set()
        elif int(message.text) <= 117 and int(user_min_age[0][0]) >= int(message.text):
            await message.answer('Максимальный возраст неправильно задан', reply_markup=close_it())
        else:
            await message.answer('Возраст слишком большой.', reply_markup=close_it())
    else:
        await message.answer('Я жду от тебя только цифры', reply_markup=close_it())
