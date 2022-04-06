from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_contact = KeyboardButton(text=f'📞Поделится контактом', request_contact=True)
send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)


def get_geo():
    send_contact = KeyboardButton(text=f'🗺 Определить автоматически', request_location=True)
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)
    return send_geo_kb


def get_photo():
    send_contact = KeyboardButton(text=f'Взять из профиля')
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)
    return send_geo_kb


def start_user_kb():
    ru_lang = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru_lang')
    en_lang = InlineKeyboardButton(text='🇬🇧 English', callback_data='en_lang')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(ru_lang, en_lang)
    return start_kb


def main_user_kb():
    find_pare = KeyboardButton(text='👩‍❤️‍👨 Найти пару')
    chat_roll = KeyboardButton(text='💬 Чат Рулетка')
    likes = KeyboardButton(text='💖 Симпатии')
    my_profile = KeyboardButton(text='👤 Моя анкета')
    compatibility = KeyboardButton(text='❤️‍🔥 Совместимость')
    premium = KeyboardButton(text='💎 Премиум')
    settings = KeyboardButton(text='⚙️ Настройка')
    bot_help = KeyboardButton(text='📌 Помощь')
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(find_pare, chat_roll)
    start_kb.add(likes, my_profile)
    start_kb.add(compatibility, premium)
    start_kb.add(settings, bot_help)
    return start_kb


def user_sex_kb():
    find_pare = KeyboardButton(text='М')
    chat_roll = KeyboardButton(text='Ж')
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(find_pare, chat_roll)
    return start_kb


def user_second_kb(cod_id=False):
    my_cod = InlineKeyboardButton(text='🛒 Мои промокоды', callback_data='my_cod')
    get_more_cod = InlineKeyboardButton(text='📝 Получить еще промокод!', callback_data='get_more_cod')
    if cod_id:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data=f'bad_cod{cod_id}')
    else:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data='bad_cod')
    start_kb = InlineKeyboardMarkup().add(my_cod)
    start_kb.add(get_more_cod)
    start_kb.add(bad_cod)
    return start_kb


def start_admin_kb():
    create_post = InlineKeyboardButton(text='📝 Разсылка 📝', callback_data='admin_sender')
    my_bot = InlineKeyboardButton(text='📊 Статистика пользователей 📊', callback_data='admin_stat')
    posts = InlineKeyboardButton(text='⚙️ Настройки ⚙️', callback_data='admin_setings')
    inform = InlineKeyboardButton(text='👥 Зайти как user 👥', callback_data='admin_as_user')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(my_bot)
    start_kb.add(posts)
    start_kb.add(inform)
    return start_kb


# отправка в рассылке без медиа
def without_media():
    back = InlineKeyboardButton(text=f'Пропустить', callback_data=f'no_data')
    user_main = InlineKeyboardMarkup()
    user_main.add(back)
    return user_main


# клавиатура для админа стартовая
def confirm(withot_back=False):
    yes_all_good = InlineKeyboardButton(text=f'Да все хорошо!', callback_data=f'yes_all_good')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    user_main.add(yes_all_good)
    if withot_back:
        return user_main
    else:
        user_main.add(back)
        return user_main


# клавиатура для админа стартовая
def choose_users():
    send_all = InlineKeyboardButton(text=f'Вообще всем', callback_data=f'send_all')
    send_en = InlineKeyboardButton(text=f'Все англоговорящие', callback_data=f'send_en')
    send_ru = InlineKeyboardButton(text=f'Все русскоговорящие', callback_data=f'send_ru')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    user_main.add(send_all)
    user_main.add(send_en)
    user_main.add(send_ru)
    user_main.add(back)
    return user_main


# Клавиатура для рассылки
def sender_kb(btns: str):
    btns = btns.split('\n')
    i = 0
    user_main = InlineKeyboardMarkup()
    while i <= len(btns) - 1:
        back = InlineKeyboardButton(text=btns[i], url=btns[i + 1])
        user_main.add(back)
        i += 2
    return user_main


# Клавиатура для под категорий
def confirm_kb(index):
    category_kb = InlineKeyboardMarkup()
    if index is None:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'back')
    else:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm_{index}')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'backsub_{index}')

    category_kb.add(confirm, back)
    return category_kb

