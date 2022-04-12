import os
import emoji

from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserProfile
from modules.functions.check_photo import search_face
from modules.keyboards import user_sex_kb, user_profile_kb, close_it, get_geo, confirm, get_photo, zodiac_kb, \
    user_verifikation_kb
from modules.functions.work_with_geo import adres_from_adres, cords_to_address
from modules.sql_func import update_db, read_by_name, join_profile_all, update_city_db
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period


def settings_text(user_id: int):
    user_data = join_profile_all(id_data=user_id)[0]

    if str(user_data[7]) == "0":
        emoji = ''
    else:
        emoji = user_data[7]

    if str(user_data[5]) == "0":
        good = '✖️ Фото не подтверждено'
    else:
        good = '✅ Фото подтверждено'

    if str(user_data[10]) == "0":
        premium = ''
    else:
        premium = '💎'

    if str(user_data[9]) == "0":
        insta = ''
    else:
        insta = f'📸<a href="https://instagram.com/{user_data[9]}">Instagram</a>\n'

    if str(user_data[8]) == "0":
        zodiac = ''
    else:
        zodiac = f'{user_data[8]}\n'

    if str(user_data[3]) == "0":
        city = ''
    else:
        city = f'🗺{user_data[3]}\n'

    if str(user_data[6]) == "0":
        description = ''
    else:
        description = f'📝{user_data[6]}\n'

    photo_id = user_data[4]

    name = user_data[1]
    age = user_data[2]
    # Собираем текст
    text = f'{emoji}{name}{premium}, {age}\n' \
           f'{good}\n' \
           f'{insta}{zodiac}{city}{description}'
    return text, photo_id


async def send_main_text(user_id: int):
    data = read_by_name(table='fast_info', name='search_status, photo_good', id_data=user_id)[0]
    status = int(data[0])
    photo = int(data[1])
    text, photo_id = settings_text(user_id)
    try:
        await bot.send_photo(caption=text, photo=photo_id, chat_id=user_id,
                             reply_markup=user_profile_kb(status, photo), parse_mode='html')
    except:
        await bot.send_message(text=text, chat_id=user_id,
                               reply_markup=user_profile_kb(status, photo), parse_mode='html')
    await UserProfile.start.set()


# Profile menu
@dp.message_handler(commands=['profile'], state='*')
@dp.message_handler(Text(equals='👤 Моя анкета', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    await send_main_text(message.from_user.id)


# Profile menu
@dp.callback_query_handler(state=UserProfile.verification, text='close_it')
@dp.callback_query_handler(state=UserProfile.zodiac, text='close_it')
@dp.callback_query_handler(state=UserProfile.about, text='close_it')
@dp.callback_query_handler(state=UserProfile.city, text='back')
@dp.callback_query_handler(state=UserProfile.name, text='close_it')
async def start_menu(call: types.CallbackQuery):
    # Send main profile text
    await send_main_text(call.from_user.id)


# Profile Name menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_name')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='👤 Напишите <b>Ваше имя:</b>', k_board=close_it())
    await UserProfile.name.set()


# Profile NAME menu
@dp.message_handler(state=UserProfile.name)
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
    update_db(name='user_name', data=message.text, id_data=message.from_user.id)
    await message.answer('Ваше имя добавлено!')
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile AGE menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_age')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🔞 Напишите <b>Ваш возраст:</b>', k_board=close_it())
    await UserProfile.age.set()


# Profile AGE menu
@dp.message_handler(state=UserProfile.age)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        user_age = int(message.text)
        if user_age < 16:
            await message.answer('Минимальный возраст 16 лет')
        elif user_age > 119:
            await message.answer('В Японии самый старый человек мира Кане Танака отпраздновала 119-летие.\n'
                                 'Ты не можешь быть таким старым!')
        else:
            update_age_period(age=user_age, tg_ig=message.from_user.id)
            update_db(table='fast_info', name='user_age', data=user_age, id_data=message.from_user.id)
            await message.answer('Ваш возраст добавлен!')
    else:
        await message.answer('Возраст должен быть только числом')
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile SEX menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_sex')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='🚻 Выберите <b>Ваш пол:</b>', k_board=user_sex_kb())
    await UserProfile.sex.set()


# Profile SEX menu
@dp.message_handler(state=UserProfile.sex)
async def start_menu(message: types.Message):
    if message.text.lower() == 'парень':
        update_db(table='fast_info', name='user_sex', data='men', id_data=message.from_user.id)
        update_db(table='fast_info', name='search_sex', data='female', id_data=message.from_user.id)
    elif message.text.lower() == 'девушка':
        update_db(table='fast_info', name='user_sex', data='female', id_data=message.from_user.id)
        update_db(table='fast_info', name='search_sex', data='men', id_data=message.from_user.id)
    else:
        await message.answer('Нажми на кнопку ниже!', reply_markup=user_sex_kb())
        return
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile CITY menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_city')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Напишите <b>Ваш город:</b>\n'
                                         'Для точного определения местоположения, нажмите кнопку ниже!',
                         k_board=get_geo())
    await UserProfile.city.set()


# Profile CITY menu
@dp.message_handler(state=UserProfile.city)
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
            update_city_db(data=city, latitude=latitude, longitude=longitude, id_data=message.from_user.id)
    except:
        return
    await UserProfile.city.set()


# Profile CITY menu
@dp.message_handler(content_types=['location'], state=UserProfile.city)
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
    update_city_db(data=address, latitude=latitude, longitude=longitude, id_data=message.from_user.id)
    await message.answer('Ваш город изменен!')
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile CITY menu
@dp.callback_query_handler(state=UserProfile.city, text='yes_all_good')
async def fill_form(call: types.CallbackQuery):
    await call.message.answer('Ваш город изменен!')
    # Send main profile text
    await send_main_text(call.from_user.id)


# Profile PHOTO menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_photo')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📷 Пришлите <b>Ваше фото</b> или установите фото из профиля Telegram.\n\n'
                                         'Если в вашем профиле нет фотографий или они скрыты настройками приватности, '
                                         'то фотография не загрузится и лучше загрузите ваше фото в ручную.',
                         k_board=get_photo(True))
    await UserProfile.photo.set()


# Profile PHOTO menu
@dp.message_handler(state=UserProfile.photo, content_types=types.ContentTypes.PHOTO)
async def fill_form(message: types.Message):
    try:
        file_name = f"{str(message.from_user.id)}.jpg"
        await message.photo[-1].download(destination_file=f'modules/functions/{file_name}')
        faces_number = search_face(file_name=file_name)
        if faces_number == 1:
            update_db(name='status', data='active', id_data=message.from_user.id)
            update_db(table='fast_info', name='photo_id', data=message.photo[-1].file_id, id_data=message.from_user.id)
            await message.answer('Ваша фотография добавлена!')
            # Send main profile text
            await send_main_text(message.from_user.id)
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
@dp.message_handler(state=UserProfile.photo)
async def fill_form(message: types.Message):
    if message.text == 'Взять из профиля':
        file_name = f"{str(message.from_user.id)}.jpg"
        photo = await message.from_user.get_profile_photos()
        if str(photo.photos) == '[]':
            faces_number = 1000
        else:
            await photo.photos[0][-1].download(destination_file=f'modules/functions/{file_name}')
            faces_number = search_face(file_name=file_name)
        if faces_number == 1:
            update_db(name='status', data='active', id_data=message.from_user.id)
            update_db(table='fast_info', name='photo_id', data=photo.photos[0][-1].file_id,
                      id_data=message.from_user.id)
            await message.answer('Ваша фотография добавлена!')
            # Send main profile text
            await send_main_text(message.from_user.id)
        else:
            await message.answer('Во время проверки вашего фото мы обнаружили подозрительный контент!\n'
                                 'Возможные причины:\n'
                                 '- на фото нет лица или не обнаружено реального человека;\n'
                                 '- на фото более одного человека;')
        if faces_number == 1000:
            return
        os.remove(f'modules/functions/{file_name}')
    elif message.text == 'Отмена':
        await message.answer('Отменено')
        await send_main_text(message.from_user.id)
    else:
        await message.answer('Я жду от тебя фото.')


# Profile ABOUT menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_about')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='📝 Расскажите о себе:\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await UserProfile.about.set()


# Profile ABOUT menu
@dp.message_handler(state=UserProfile.about)
async def start_menu(message: types.Message):
    update_db(table='fast_info', name='about_text', data=message.text, id_data=message.from_user.id)
    await message.answer('Добавлено!')
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile EMOJI menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_emoji')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Отправьте эмодзи, который хотите поставить перед своим именем!\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await UserProfile.emoji.set()


# Profile EMOJI menu
@dp.message_handler(state=UserProfile.emoji)
async def start_menu(message: types.Message):
    if emoji.demojize(message.text).startswith(':') and emoji.demojize(message.text).endswith(':'):
        update_db(table='fast_info', name='emoji', data=message.text, id_data=message.from_user.id)
        await message.answer('Добавлено!')
        # Send main profile text
        await send_main_text(message.from_user.id)
    elif message.text == '0':
        update_db(table='fast_info', name='emoji', data=message.text, id_data=message.from_user.id)
        await message.answer('Удалено!')
        # Send main profile text
        await send_main_text(message.from_user.id)
    else:
        await message.answer('Нельзя добавлять текст! Пришлите пожалуйста emoji!')


# Profile ZODIAC menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_zodiac')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer(text='Выберите ваш знак:', reply_markup=zodiac_kb())
    await UserProfile.zodiac.set()


# Profile ZODIAC menu
@dp.callback_query_handler(state=UserProfile.zodiac)
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
    update_db(table='fast_info', name='zodiac', data=zodiac, id_data=call.from_user.id)
    await call.message.answer('Добавлено!')
    # Send main profile text
    await send_main_text(call.from_user.id)


# Profile INSTAGRAM menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_insta')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Пришлите ваш никнейм в Instagram\n'
                                         'Пример: <b>durov</b>\n'
                                         'Если хотите удалить это поле, отправьте 0.\n'
                                         'Пример: <b>0</b>', k_board=close_it())
    await UserProfile.Instagram.set()


# Profile INSTAGRAM menu
@dp.message_handler(state=UserProfile.Instagram)
async def start_menu(message: types.Message):
    update_db(table='fast_info', name='instagram', data=message.text, id_data=message.from_user.id)
    if message.text == '0':
        await message.answer('Ваш инстаграм удален!')
    else:
        await message.answer('Ваш инстаграм добавлен!')
    # Send main profile text
    await send_main_text(message.from_user.id)


# Profile Close/Open profile menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_close')
async def start_menu(call: types.CallbackQuery):
    status = read_by_name(table='fast_info', name='search_status', id_data=call.from_user.id)[0][0]
    if status == 0:
        update_db(table='fast_info', name='search_status', data=1, id_data=call.from_user.id)
        await edit_text_call(call=call, text='🙋Вы показали свою анкету в поиске!')
    else:
        update_db(table='fast_info', name='search_status', data=0, id_data=call.from_user.id)
        await edit_text_call(call=call, text='🙅Вы скрыли свою анкету в поиске!')
    # Send main profile text
    await send_main_text(call.from_user.id)


# Profile Close/Open profile menu
@dp.callback_query_handler(state=UserProfile.start, text='profile_good')
async def start_menu(call: types.CallbackQuery):
    photo_id = 'AgACAgIAAxkBAAIMP2JS1kOXbq8h1O1NoDg1L04NXPaVAAJvvjEb1JeRSiI8rJlH0iwVAQADAgADcwADIwQ'
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo_id, parse_mode='html',
                         caption='Ваше фото не подтверждено, чтобы получить галочку, вам нужно отправить '
                                 'Вашу фотографию как показано на этом примере, не волнуйтесь, её никто не '
                                 'увидит, она необходима только для верификации.\n\n'
                                 '<b>Важно, у вас должна быть рука именно в таком же положение иначе бот не '
                                 'сможет одобрить вам верификацию!</b>', reply_markup=close_it())
    await UserProfile.verification.set()


# Start menu
@dp.message_handler(state=UserProfile.verification, content_types=types.ContentType.PHOTO)
async def start_menu(message: types.Message):
    await message.answer('Ваше фото Отправлено на верификацию')
    await bot.send_photo(chat_id=constant.admin(), photo=message.photo[0].file_id,
                         caption=f'Пользователь с id: {message.from_user.id}',
                         reply_markup=user_verifikation_kb(message.from_user.id))
    await UserProfile.start.set()
