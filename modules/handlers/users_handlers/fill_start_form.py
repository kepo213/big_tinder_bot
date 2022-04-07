import os

from aiogram import types
from main import dp
from modules.functions.check_photo import search_face
from modules.functions.work_with_geo import adres_from_adres, cords_to_address
from aiogram.dispatcher.filters import Text
from modules.handlers.handlers_func import edit_text_call
from modules.sql_func import insert_user, read_by_name, all_users_table, \
    update_db, create_fast_info_table, sender_table, read_all
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin, User
from aiogram.dispatcher import FSMContext
from modules.keyboards import user_sex_kb, get_geo, get_photo, confirm, main_user_kb


@dp.callback_query_handler(state=User.start)
async def fill_form(call: types.CallbackQuery):
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
async def fill_form(message: types.Message):
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
        update_db(name='user_name', data=message.text, id_data=message.from_user.id)
        await message.answer('🔞 Напишите <b>Ваш возраст</b>:', parse_mode='html')
        await User.set_age.set()
    else:
        await message.answer('В вашем имени есть недопустимые слова!')


@dp.message_handler(state=User.set_age)
async def fill_form(message: types.Message):
    if message.text.isdigit():
        user_age = int(message.text)
        if user_age < 16:
            await message.answer('Минимальный возраст 16 лет')
        elif user_age > 119:
            await message.answer('В Японии самый старый человек мира Кане Танака отпраздновала 119-летие.\n'
                                 'Ты не можешь быть таким старым!')
        else:
            update_db(table='fast_info', name='user_age', data=user_age, id_data=message.from_user.id)
            await message.answer('🚻 Выберите <b>Ваш пол:</b>', parse_mode='html', reply_markup=user_sex_kb())
            await User.set_sex.set()
    else:
        await message.answer('Возраст должен быть только числом')


@dp.message_handler(state=User.set_sex)
async def fill_form(message: types.Message):
    if message.text.lower() == 'парень':
        update_db(table='fast_info', name='user_sex', data='men', id_data=message.from_user.id)
    elif message.text.lower() == 'девушка':
        update_db(table='fast_info', name='user_sex', data='female', id_data=message.from_user.id)
    else:
        await message.answer('Нажми на кнопку ниже!', reply_markup=user_sex_kb())
        return
    await message.answer('Напишите <b>Ваш город:</b>\n'
                         'Для точного определения местоположения, нажмите кнопку ниже!', reply_markup=get_geo(),
                         parse_mode='html')
    await User.set_geo.set()


# receive the address of user's home
@dp.message_handler(content_types=['location'], state=User.set_geo)
async def fill_form(message: types.Message):
    x = message.location.latitude
    y = message.location.longitude
    address = cords_to_address(x=x, y=y)
    if address == 'Error':
        await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
        return
    address = adres_from_adres(address)
    if address == 'Error':
        await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
        return
    update_db(table='fast_info', name='city', data=address, id_data=message.from_user.id)
    await message.answer('📷 Пришлите <b>Ваше фото</b> или установите фото из профиля Telegram.\n'
                         'Если в вашем профиле нет фотографий или они скрыты настройками приватности, то '
                         'фотография не загрузится и лучше загрузите ваше фото в ручную.',
                         parse_mode='html', reply_markup=get_photo())
    await User.set_photo.set()


@dp.message_handler(state=User.set_geo)
async def fill_form(message: types.Message):
    try:
        city = adres_from_adres(message.text)
        if city == 'Error':
            await message.answer('❌ Мы не нашли такого города, возможно вы ввели его с ошибками')
            return
        else:
            await message.answer(f'Я нашел такой адрес:\n'
                                 f'<b>{city}</b>\n'
                                 f'Если все правильно то подтвердите.', reply_markup=confirm(True), parse_mode='html')
            update_db(table='fast_info', name='city', data=city, id_data=message.from_user.id)
            await User.set_geo.set()
    except:
        pass


@dp.callback_query_handler(state=User.set_geo, text='yes_all_good')
async def fill_form(call: types.CallbackQuery):
    await call.message.answer('📷 Пришлите <b>Ваше фото</b> или установите фото из профиля Telegram.\n'
                              'Если в вашем профиле нет фотографий или они скрыты настройками приватности, то '
                              'фотография не загрузится и лучше загрузите ваше фото в ручную.',
                              parse_mode='html', reply_markup=get_photo())
    await User.set_photo.set()


@dp.message_handler(state=User.set_photo, content_types=types.ContentTypes.PHOTO)
async def fill_form(message: types.Message):
    try:
        file_name = f"{str(message.from_user.id)}.jpg"
        await message.photo[-1].download(destination_file=f'modules/functions/{file_name}')
        faces_number = search_face(file_name=file_name)
        if faces_number == 1:
            update_db(name='status', data='active', id_data=message.from_user.id)
            update_db(table='fast_info', name='photo_id', data=message.photo[-1].file_id, id_data=message.from_user.id)
            await message.answer('✅ Регистрация вашей анкеты завершена!\n'
                                 '👩‍❤️‍👨 Чтобы найти пару воспользуйтесь меню ниже, или командой: /love\n'
                                 '📂 Команда для вызова меню: /start', reply_markup=main_user_kb())
            await User.start.set()
        else:
            await message.answer('Во время проверки вашего фото мы обнаружили подозрительный контент!\n'
                                 'Возможные причины:\n'
                                 '- на фото нет лица или не обнаружено реального человека;\n'
                                 '- высокий процент наготы;\n'
                                 '- на фото более одного человека;')
        os.remove(f'modules/functions/{file_name}')
    except:
        pass


@dp.message_handler(state=User.set_photo)
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
            update_db(table='fast_info', name='photo_id', data=photo.photos[0][-1].file_id, id_data=message.from_user.id)
            await message.answer('✅ Регистрация вашей анкеты завершена!\n'
                                 '👩‍❤️‍👨 Чтобы найти пару воспользуйтесь меню ниже, или командой: /love\n'
                                 '📂 Команда для вызова меню: /start', reply_markup=main_user_kb())
        else:
            await message.answer('Во время проверки вашего фото мы обнаружили подозрительный контент!\n'
                                 'Возможные причины:\n'
                                 '- на фото нет лица или не обнаружено реального человека;\n'
                                 '- на фото более одного человека;')
        if faces_number == 1000:
            return
        os.remove(f'modules/functions/{file_name}')
    else:
        await message.answer('Я жду от тебя фото.')
