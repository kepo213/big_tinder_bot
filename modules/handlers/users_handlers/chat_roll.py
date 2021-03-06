import datetime

from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserChatRoll
from modules.keyboards import chat_roll, chat_roll_start, users_score_kb, chat_settings, stop_chat_roll
from modules.sql_func import update_db, read_by_name, join_chat_stata, count_refs_for_chats, join_chat_data, \
    grow_chat_chats_db, count_chats, \
    join_chat_data_sex, count_all_active_chat_roll
from modules.functions.simple_funcs import chat_roll_score


# Profile menu
@dp.message_handler(commands=['chat'], state='*')
@dp.message_handler(Text(equals='❌🔍 Остановить поиск!', ignore_case=True), state=UserChatRoll.start)
@dp.message_handler(Text(equals='🔙Главное меню', ignore_case=True), state=UserChatRoll.settings)
@dp.message_handler(Text(equals='💬 Чат Рулетка', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    count_chat_users = count_chats()[0][0]
    active_chat_users = count_all_active_chat_roll()[0][0]
    await message.answer(f'💬 Чат Рулетка\n\n'
                         f'🙋‍♂️Активные за 24 часа: {active_chat_users}\n'
                         f'👥 Сейчас пользователей онлайн: {count_chat_users}', parse_mode='html',
                         reply_markup=chat_roll())
    await UserChatRoll.start.set()


# Profile menu
@dp.message_handler(Text(equals='💬 Запустить чат рулетку', ignore_case=True), state=UserChatRoll.start)
async def start_menu(message: types.Message):
    premium = read_by_name(table='fast_info', name='premium', id_data=message.from_user.id)[0][0]
    karma = read_by_name(table='chat_roll', name='karma', id_data=message.from_user.id)[0][0]
    if karma <= -10:
        return await message.answer(f'Вам ограничен доступ к «Чат рулетке» по причине отрицательной кармы 😢\n'
                                    f'<b>😭 Ваша карма: {karma}</b>\n'
                                    f'<em>Не расстраивайтесь, вы можете обнулить свою карму пригласив 30 друзей. '
                                    f'Ваша пригласительная ссылка: тут ссылка</em>', parse_mode='html')
    elif -10 < karma < 0:
        await message.answer(f'<b>😭 Ваша карма: {karma}</b>\n'
                             f'<em>Ваша карма отрицательная, при достижении -10 вам будет ограничен доступ к '
                             f'Чат-рулетке!</em>', parse_mode='html')
    elif 0 < karma < 10:
        await message.answer(f'<b>🙂 Ваша карма: {karma}</b>\n'
                             f'<em>Вы хороший собеседник!</em>', parse_mode='html')
    elif 10 < karma:
        await message.answer(f'<b>😍 Ваша карма: {karma}</b>\n'
                             f'<em>Вы хороший собеседник!</em>', parse_mode='html')

    update_db(table="chat_roll", name="status", data=1, id_data=message.from_user.id)
    update_db(table="chat_roll", name="activity", data=datetime.datetime.now(), id_data=message.from_user.id)
    await message.answer('Ищу собеседника... 🔍', reply_markup=stop_chat_roll())
    if int(premium) == 1:
        search_sex = read_by_name(table='fast_info', name='search_sex', id_data=message.from_user.id)[0][0]
        if str(search_sex) == 'all':
            chat_data = join_chat_data(tg_id=message.from_user.id)
        else:
            chat_data = join_chat_data_sex(tg_id=message.from_user.id, sex=str(search_sex))
    else:
        chat_data = join_chat_data(tg_id=message.from_user.id)
    if str(chat_data) == '[]':
        return
    else:
        friend_id = '[]'
        for user in chat_data:
            friend_id = user[0]
            premium = read_by_name(table='fast_info', name='premium', id_data=friend_id)[0][0]
            if int(premium) == 0:
                break
            else:
                search_sex = read_by_name(table='fast_info', name='search_sex', id_data=friend_id)[0][0]
                if str(search_sex) == str(user[2]):
                    break
                else:
                    friend_id = '[]'
        if friend_id == '[]':
            return
        grow_chat_chats_db(message.from_user.id)
        grow_chat_chats_db(friend_id)
        update_db(table="chat_roll", name="status", data=0, id_data=message.from_user.id)
        update_db(table="chat_roll", name="status", data=0, id_data=friend_id)
        update_db(table="chat_roll", name="friend_id", data=friend_id, id_data=message.from_user.id)
        update_db(table="chat_roll", name="friend_id", data=message.from_user.id, id_data=friend_id)
        await bot.send_message(chat_id=friend_id, text='Нашёл кое-кого для тебя! 🥝\n',
                               reply_markup=chat_roll_start())
        await message.answer('Нашёл кое-кого для тебя! 🥝\n', reply_markup=chat_roll_start())

    await UserChatRoll.talk.set()


# Profile menu
@dp.message_handler(Text(equals='📈 Моя статистика', ignore_case=True), state=UserChatRoll.start)
async def start_menu(message: types.Message):
    user_data = join_chat_stata(id_data=message.from_user.id)[0]
    chat_data = read_by_name(table='chat_roll', name='messages, chats, karma', id_data=message.from_user.id)[0]
    refs = count_refs_for_chats(tg_id=message.from_user.id)[0][0]
    if str(user_data[1]) == 'men':
        sex = 'М'
    else:
        sex = 'Ж'
    await message.answer(f'#️⃣ ID — {message.from_user.id}\n\n'
                         f'👤 Имя — {user_data[0]}\n'
                         f'👫 Пол — {sex}\n'
                         f'🔞 Возраст — от {user_data[2]} до {user_data[3]} лет\n'
                         f'🌎 Город — {user_data[4]}\n\n'
                         f'📧 Сообщений — {chat_data[0]}\n\n'
                         f'💬 Чатов — {chat_data[1]}\n'
                         f'👁️ Карма — {chat_data[2]}\n'
                         f'🎪 Приглашено пользователей — {refs}', parse_mode='html',
                         reply_markup=chat_roll())
    await UserChatRoll.start.set()


# Profile menu
@dp.message_handler(Text(equals='🏆 Рейтинг', ignore_case=True), state=UserChatRoll.start)
async def start_menu(message: types.Message):
    await message.answer(f'🏆 Рейтинг', parse_mode='html',
                         reply_markup=users_score_kb())
    await UserChatRoll.score.set()


@dp.callback_query_handler(state=UserChatRoll.score, text_contains='chat_score_karma')
async def start_menu(call: types.CallbackQuery):
    text = chat_roll_score(key='karma')
    await call.message.answer(f'🏆 Рейтинг\n👁 По карме\n{text}', parse_mode='html')


@dp.callback_query_handler(state=UserChatRoll.score, text_contains='chat_score_messages')
async def start_menu(call: types.CallbackQuery):
    text = chat_roll_score(key='messages')
    await call.message.answer(f'🏆 Рейтинг\n📧 По сообщениям\n{text}', parse_mode='html')


@dp.callback_query_handler(state=UserChatRoll.score, text_contains='chat_score_dialogs')
async def start_menu(call: types.CallbackQuery):
    text = chat_roll_score(key='chats')
    await call.message.answer(f'🏆 Рейтинг\n💬 По диалогам\n{text}', parse_mode='html')


# Profile menu
@dp.message_handler(Text(equals='⚙️ Настройки поиска', ignore_case=True), state=UserChatRoll.start)
async def start_menu(message: types.Message):
    premium_status = read_by_name(table='fast_info', name='premium', id_data=message.from_user.id)[0][0]
    if int(premium_status) == 0:
        count_chat_users = count_chats()[0][0]
        await message.answer('💎Этот раздел только для премиум пользователей.')
        await message.answer(f'👥 Сейчас пользователей онлайн: {count_chat_users}', parse_mode='html',
                             reply_markup=chat_roll())
        await UserChatRoll.start.set()
        return
    await message.answer(f'⚙️ Настройки поиска.', parse_mode='html',
                         reply_markup=chat_settings())
    await UserChatRoll.settings.set()


# Profile menu
@dp.message_handler(Text(equals='👩 Поиск среди девушек', ignore_case=True), state=UserChatRoll.settings)
@dp.message_handler(Text(equals='👨 Поиск среди парней', ignore_case=True), state=UserChatRoll.settings)
@dp.message_handler(Text(equals='👨👩 Поиск среди всех', ignore_case=True), state=UserChatRoll.settings)
async def start_menu(message: types.Message):
    if message.text == '👩 Поиск среди девушек':
        text = 'Установлен поиск среди 👩девушек'
        update_db(table='fast_info', name='search_sex', data='female', id_data=message.from_user.id)
    elif message.text == '👨 Поиск среди парней':
        update_db(table='fast_info', name='search_sex', data='men', id_data=message.from_user.id)
        text = 'Установлен поиск среди 👨парней'
    elif message.text == '👨👩 Поиск среди всех':
        update_db(table='fast_info', name='search_sex', data='all', id_data=message.from_user.id)
        text = 'Установлен поиск среди 👨👩всех'
    else:
        return
    await message.answer(text)
    count_chat_users = count_chats()[0][0]
    await message.answer(f'👥 Сейчас пользователей онлайн: {count_chat_users}', parse_mode='html',
                         reply_markup=chat_roll())
    await UserChatRoll.start.set()
