from aiogram import types
from main import dp
from modules.dispatcher import constant
from aiogram.dispatcher.filters import Text

from modules.dispatcher import bot, UserChatRoll, UserCouples
from modules.handlers.users_handlers.find_couples import show_other_profile
from modules.keyboards import chat_roll, chat_roll_start
from modules.sql_func import update_db, read_by_name, search_person, join_profile_all, read_all_2, \
    insert_likes_presents_db, join_chat_stata, count_refs_for_chats, join_chat_data, grow_chat_chats_db, count_chats
from modules.handlers.handlers_func import edit_text_call
from modules.functions.simple_funcs import update_age_period, get_right_left_btn


# Profile menu
@dp.message_handler(commands=['chat'], state='*')
@dp.message_handler(Text(equals='💬 Чат Рулетка', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    count_chat_users = count_chats()[0][0]
    await message.answer(f'👥 Сейчас пользователей онлайн: {count_chat_users}', parse_mode='html',
                         reply_markup=chat_roll())
    await UserChatRoll.start.set()


# Profile menu
@dp.message_handler(Text(equals='💬 Запустить чат рулетку', ignore_case=True), state=UserChatRoll.start)
async def start_menu(message: types.Message):
    update_db(table="chat_roll", name="status", data=1, id_data=message.from_user.id)
    await message.answer('Ищу собеседника... 🔍')
    chat_data = join_chat_data(tg_id=message.from_user.id)
    if str(chat_data) == '[]':
        return
    else:
        friend_id = chat_data[0][0]
        grow_chat_chats_db(message.from_user.id)
        grow_chat_chats_db(friend_id)
        update_db(table="chat_roll", name="status", data=0, id_data=message.from_user.id)
        update_db(table="chat_roll", name="status", data=0, id_data=friend_id)
        update_db(table="chat_roll", name="friend_id", data=friend_id, id_data=message.from_user.id)
        update_db(table="chat_roll", name="friend_id", data=message.from_user.id, id_data=friend_id)
        await bot.send_message(chat_id=friend_id, text='Нашёл кое-кого для тебя! 🥝\n'
                                                       '/stop - Остановить диалог',
                               reply_markup=chat_roll_start())
        await message.answer('Нашёл кое-кого для тебя! 🥝\n'
                             '/stop - Остановить диалог', reply_markup=chat_roll_start())

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
