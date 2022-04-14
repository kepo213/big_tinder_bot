from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

send_contact = KeyboardButton(text=f'📞Поделится контактом', request_contact=True)
send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)


def get_geo():
    send_contact = KeyboardButton(text=f'🗺 Определить автоматически', request_location=True)
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)
    return send_geo_kb


def get_photo(close_it: bool = False):
    send_contact = KeyboardButton(text=f'Взять из профиля')
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if close_it:
        close_it_btn = KeyboardButton(text=f'Отмена')
        send_geo_kb.add(send_contact, close_it_btn)
    else:
        send_geo_kb.add(send_contact)
    return send_geo_kb


def reff_kb(url: str, back: bool = False):
    ru_lang = InlineKeyboardButton(text='🫂Пригласить друга',
                                   switch_inline_query=f"❤️‍🔥Вас пригласили в бот знакомств:\n\n{url}")
    en_lang = InlineKeyboardButton(text='Параметры', callback_data='premium_reff')
    back_btn = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup()
    if back:
        start_kb.add(ru_lang, back_btn)
    else:
        start_kb.add(ru_lang, en_lang)
    return start_kb


def start_user_kb():
    ru_lang = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru_lang')
    en_lang = InlineKeyboardButton(text='🇺🇸 English', callback_data='en_lang')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(ru_lang, en_lang)
    return start_kb


def user_verifikation_kb(user_id: int):
    verifikation = InlineKeyboardButton(text='Подтвердить', callback_data=f'verifikation_{user_id}')
    verifikation_close = InlineKeyboardButton(text='Отклонить', callback_data=f'verifikation_close_{user_id}')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(verifikation, verifikation_close)
    return start_kb


def user_couples_kb(user_id: int):
    yes = InlineKeyboardButton(text='💚 Like', callback_data=f'couple_yes_{user_id}')
    present = InlineKeyboardButton(text='🎁', callback_data=f'couple_present_{user_id}')
    no = InlineKeyboardButton(text='💔 Skip', callback_data=f'couple_no_{user_id}')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(yes, present, no)
    return start_kb


def user_couples_adv_kb(url: str):
    yes = InlineKeyboardButton(text='💚 Like', url=url)
    no = InlineKeyboardButton(text='💔 Skip', callback_data=f'couple_no_adv')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(yes, no)
    return start_kb


def user_like_like_adv_kb(user_id: int):
    yes = InlineKeyboardButton(text='👍 покажи', callback_data=f'couple_double_yes_{user_id}')
    no = InlineKeyboardButton(text='👎 пропустить', callback_data=f'couple_double_no')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(yes, no)
    return start_kb


def compotibility_kb():
    ru_lang = InlineKeyboardButton(text='❤️‍🔥 Проверить совместимость',
                                   url='https://t.me/BeRelaxBot?start=compatibility_ru')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(ru_lang)
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


def user_profile_kb(status: int, photo: int):
    profile_name = InlineKeyboardButton(text='👤 Имя', callback_data='profile_name')
    profile_age = InlineKeyboardButton(text='🔞 Возраст', callback_data='profile_age')
    profile_sex = InlineKeyboardButton(text='🚻 Пол:', callback_data='profile_sex')

    profile_city = InlineKeyboardButton(text='🌍 Город', callback_data='profile_city')
    profile_photo = InlineKeyboardButton(text='📷 Фото', callback_data='profile_photo')
    profile_about = InlineKeyboardButton(text='📝 О себе', callback_data='profile_about')

    profile_emoji = InlineKeyboardButton(text='Эмодзи', callback_data='profile_emoji')
    profile_zodiac = InlineKeyboardButton(text='☯️ Знак зодиака', callback_data='profile_zodiac')
    profile_insta = InlineKeyboardButton(text='📸 Instagram', callback_data='profile_insta')

    # profile_gallery = InlineKeyboardButton(text='🎑 Галерея', callback_data='profile_gallery')
    if status == 1:
        profile_close = InlineKeyboardButton(text='🙅Скрыть анкету', callback_data='profile_close')
    else:
        profile_close = InlineKeyboardButton(text='🙋Показать анкету', callback_data='profile_close')

    profile_good = InlineKeyboardButton(text='✖️ Фото не подтверждено', callback_data='profile_good')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(profile_name, profile_age, profile_sex)
    start_kb.add(profile_city, profile_photo, profile_about)
    start_kb.add(profile_emoji, profile_zodiac, profile_insta)
    start_kb.add(profile_close)
    if photo == 0:
        start_kb.add(profile_good)
    else:
        pass
    return start_kb


# клавиатура на ru для сна
def zodiac_kb():
    aries = InlineKeyboardButton(text=f'♈️ Овен', callback_data='zodiac_aries')
    taurus = InlineKeyboardButton(text=f'♉️ Телец', callback_data='zodiac_taurus')
    gemini = InlineKeyboardButton(text=f'♊️ Близнецы', callback_data='zodiac_gemini')

    cancer = InlineKeyboardButton(text=f'♋️ Рак', callback_data='zodiac_cancer')
    leo = InlineKeyboardButton(text=f'♌️ Лев', callback_data='zodiac_leo')
    virgo = InlineKeyboardButton(text=f'♍️ Дева', callback_data='zodiac_virgo')

    libra = InlineKeyboardButton(text=f'♎️ Весы', callback_data='zodiac_libra')
    scorpio = InlineKeyboardButton(text=f'♏️ Скорпион', callback_data='zodiac_scorpio')
    sagittarius = InlineKeyboardButton(text=f'♐️ Стрелец', callback_data='zodiac_sagittarius')

    capricorn = InlineKeyboardButton(text=f'♑️ Козерог', callback_data='zodiac_capricorn')
    aquarius = InlineKeyboardButton(text=f'♒️ Водолей', callback_data='zodiac_aquarius')
    pisces = InlineKeyboardButton(text=f'♓️ Рыбы', callback_data='zodiac_pisces')
    go_to_main = InlineKeyboardButton(text=f'Отмена', callback_data=f'close_it')
    clear = InlineKeyboardButton(text=f'🗑Очистить', callback_data=f'clear')
    user_main = InlineKeyboardMarkup().add(aries, taurus, gemini)
    user_main.add(cancer, leo, virgo)
    user_main.add(libra, scorpio, sagittarius)
    user_main.add(capricorn, aquarius, pisces)
    user_main.add(go_to_main, clear)
    return user_main


def user_sex_kb():
    find_pare = KeyboardButton(text='Парень')
    chat_roll = KeyboardButton(text='Девушка')
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(find_pare, chat_roll)
    return start_kb


def user_settings_kb():
    user_age_period = InlineKeyboardButton(text='🔞 Возр.диапазон', callback_data='user_age_period')
    get_more_cod = InlineKeyboardButton(text='🌐 Макс.расстояние', callback_data='user_max_range')
    user_language = InlineKeyboardButton(text='🏳️ Язык/Language', callback_data=f'user_language')
    start_kb = InlineKeyboardMarkup().add(user_age_period)
    start_kb.add(get_more_cod)
    start_kb.add(user_language)
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


def admins_settings_kb():
    admin_setings_adv_m = InlineKeyboardButton(text='📺🙎‍♂️ Реклама М', callback_data='admin_setings_adv_m')
    admin_setings_adv_f = InlineKeyboardButton(text='📺🙍🏻‍♀️ Реклама Ж', callback_data='admin_setings_adv_f')
    admin_setings_adv_number = InlineKeyboardButton(text='📺 Частота рекламы', callback_data='admin_setings_adv_number')
    admin_setings_fake_number = InlineKeyboardButton(text='🌠Частота фэйковых анкет',
                                                     callback_data='admin_settings_fake_number')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(admin_setings_adv_m)
    start_kb.add(admin_setings_adv_f)
    start_kb.add(admin_setings_adv_number)
    start_kb.add(admin_setings_fake_number)
    start_kb.add(back)
    return start_kb


# отправка в рассылке без медиа
def without_media():
    back = InlineKeyboardButton(text=f'Пропустить', callback_data=f'no_data')
    user_main = InlineKeyboardMarkup()
    user_main.add(back)
    return user_main


def close_it():
    back = InlineKeyboardButton(text=f'Отмена', callback_data=f'close_it')
    user_main = InlineKeyboardMarkup()
    user_main.add(back)
    return user_main


# клавиатура для админа стартовая
def confirm(without_back=False, without_yes=False, ):
    yes_all_good = InlineKeyboardButton(text=f'Да все хорошо!', callback_data=f'yes_all_good')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    if without_yes:
        pass
    else:
        user_main.add(yes_all_good)
    if without_back:
        pass
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
