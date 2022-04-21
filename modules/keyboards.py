from modules.sql_func import join_likes, read_by_name, join_get_bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

send_contact = KeyboardButton(text=f'📞Поделится контактом', request_contact=True)
send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)


def get_geo():
    send_contact = KeyboardButton(text=f'🗺 Определить автоматически', request_location=True)
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)
    return send_geo_kb


def chat_roll_start():
    start_roll = KeyboardButton(text=f'❌ Остановить!')
    my_stat = KeyboardButton(text=f'👤 Показать свой профиль')
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(start_roll, my_stat)
    return send_geo_kb


def chat_roll():
    start_roll = KeyboardButton(text=f'💬 Запустить чат рулетку')
    my_stat = KeyboardButton(text=f'📈 Моя статистика')
    score = KeyboardButton(text=f'🏆 Рейтинг')
    settings = KeyboardButton(text=f'⚙️ Настройки поиска')
    main_menu = KeyboardButton(text=f'🔙Главное меню')
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(start_roll, my_stat)
    send_geo_kb.add(score, settings)
    return send_geo_kb.add(main_menu)


def chat_settings():
    guys = KeyboardButton(text=f'👨 Поиск среди парней')
    girls = KeyboardButton(text=f'👩 Поиск среди девушек')
    guys_and_girls = KeyboardButton(text=f'👨👩 Поиск среди всех')
    main_menu = KeyboardButton(text=f'🔙Главное меню')
    send_geo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(guys)
    send_geo_kb.add(girls)
    send_geo_kb.add(guys_and_girls)
    return send_geo_kb.add(main_menu)


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


def user_likes_kb():
    double_like = InlineKeyboardButton(text='👍 Взаимный лайк', callback_data='user_double_likes')
    you_likes = InlineKeyboardButton(text='👍 Вы лайкнули', callback_data='user_you_likes')
    user_likes = InlineKeyboardButton(text='👍 Вас лайкнули', callback_data='user_likes')
    user_presents_send = InlineKeyboardButton(text='🎁 Кому отправил', callback_data='user_presents_send')
    user_presents_from = InlineKeyboardButton(text='🎁 От кого получил', callback_data='user_presents_from')
    start_kb = InlineKeyboardMarkup().add(double_like)
    start_kb.add(you_likes)
    start_kb.add(user_likes)
    start_kb.add(user_presents_send)
    start_kb.add(user_presents_from)
    return start_kb


def chat_likes_kb(tg_id: int, status: bool = True):
    user_presents_send = InlineKeyboardButton(text='🎁', callback_data=f'markchat_present_{tg_id}')
    if status:
        pass
    else:
        tg_id = 'click'
    user_likes = InlineKeyboardButton(text='👍', callback_data=f'markchat_good_{tg_id}')
    user_presents_from = InlineKeyboardButton(text='👎', callback_data=f'markchat_bad_{tg_id}')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(user_likes, user_presents_send, user_presents_from)
    return start_kb


def likes_kb(users: tuple):
    start_kb = InlineKeyboardMarkup()
    for user in users:
        user_data = join_likes(int(user[0]))[0]

        btn_text = f"{user_data[1]}, {user_data[2]}, {user_data[3]}"
        user_likes = InlineKeyboardButton(text=btn_text, callback_data=f'like_kb_{user_data[0]}')
        start_kb.add(user_likes)
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb.add(back)
    return start_kb


def likes_in_profile_kb(this_: str, left: bool = False, right: bool = False):
    start_kb = InlineKeyboardMarkup()
    if left:
        left_btn = InlineKeyboardButton(text=f'◀️', callback_data=f'like_kb_{left}')
    else:
        left_btn = InlineKeyboardButton(text=f'⏺', callback_data=f'like_kb_stop')

    if right:
        right_btn = InlineKeyboardButton(text=f'▶️', callback_data=f'like_kb_{right}')
    else:
        right_btn = InlineKeyboardButton(text=f'⏺', callback_data=f'like_kb_stop')

    delete = InlineKeyboardButton(text=f'🗑 Удалить', callback_data=f'like_kb_delete_{this_}')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    if not left and not right:
        pass
    else:
        start_kb.add(left_btn, right_btn)
    start_kb.add(delete, back)
    return start_kb


def user_verifikation_kb(user_id: int):
    verifikation = InlineKeyboardButton(text='Подтвердить', callback_data=f'verifikation_{user_id}')
    verifikation_close = InlineKeyboardButton(text='Отклонить', callback_data=f'verifikation_close_{user_id}')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(verifikation, verifikation_close)
    return start_kb


def user_couples_kb(user_id: int, presents: int):
    yes = InlineKeyboardButton(text='💚 Like', callback_data=f'couple_yes_{user_id}')
    present = InlineKeyboardButton(text=f'🎁({presents})', callback_data=f'couple_present_{user_id}')
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


def users_score_kb():
    chat_score_karma = InlineKeyboardButton(text='👁 По карме', callback_data='chat_score_karma')
    chat_score_messages = InlineKeyboardButton(text='📧 По сообщениям', callback_data='chat_score_messages')
    chat_score_dialogs = InlineKeyboardButton(text='💬 По диалогам', callback_data='chat_score_dialogs')
    start_kb = InlineKeyboardMarkup(resize_keyboard=True)
    start_kb.add(chat_score_karma, chat_score_messages)
    start_kb.add(chat_score_dialogs)
    return start_kb


def user_profile_kb(status: int, photo: int, delete: bool = False):
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
    if delete:
        profile_good = InlineKeyboardButton(text='Подтвердить фото', callback_data='profile_good')
        delete_bot = InlineKeyboardButton(text='❌🗑 Удалить бот 🤖', callback_data='delete_bot')
        start_kb.add(delete_bot, profile_good)
    else:
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
    create_post = InlineKeyboardButton(text='📝 Рассылка 📝', callback_data='admin_sender')
    my_bot = InlineKeyboardButton(text='📊 Статистика пользователей 📊', callback_data='admin_stat')
    adv = InlineKeyboardButton(text='⚙️ Настройки рекламы ⚙️', callback_data='admin_adv_setings')
    auto_sender = InlineKeyboardButton(text='📝🤖 Авто рассылка', callback_data='auto_sender')
    inform = InlineKeyboardButton(text='👥 Зайти как user 👥', callback_data='admin_as_user')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(my_bot)
    start_kb.add(adv)
    start_kb.add(auto_sender)
    start_kb.add(inform)
    return start_kb


def smart_sender():
    create_post = InlineKeyboardButton(text='📝 Новый пост ✈️', callback_data='new_post')
    adv = InlineKeyboardButton(text='✈️📝 Все посты рассылки', callback_data='admin_smart_sender')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(adv)
    start_kb.add(back)
    return start_kb


def smart_sender_post_type():
    create_post = InlineKeyboardButton(text='Отсчет от регистрации', callback_data='new_post_first_reg')
    adv = InlineKeyboardButton(text='От последней активности', callback_data='new_post_lust_active')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(adv)
    start_kb.add(back)
    return start_kb


def pick_sex():
    create_post = InlineKeyboardButton(text='Для парней', callback_data='for_mans')
    adv = InlineKeyboardButton(text='Для девушек', callback_data='for_females')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(adv)
    return start_kb


def admins_settings_kb():
    admin_setings_adv_couples = InlineKeyboardButton(text='📺Реклама в "Найти пару"',
                                                     callback_data='admin_setings_adv_couples')
    admin_setings_adv_chat_roll = InlineKeyboardButton(text='📺Реклама в "Чат рулетке"',
                                                       callback_data='admin_setings_adv_chat_roll')
    admin_settings_fake_people = InlineKeyboardButton(text='🌠Фэйковые анкеты',
                                                      callback_data='admin_settings_fake_people')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(admin_setings_adv_couples)
    start_kb.add(admin_setings_adv_chat_roll)
    start_kb.add(admin_settings_fake_people)
    start_kb.add(back)
    return start_kb


def admins_settings_adv_only():
    admin_setings_adv_m = InlineKeyboardButton(text='📺🙎‍♂️ Реклама М', callback_data='admin_setings_adv_m')
    admin_setings_adv_f = InlineKeyboardButton(text='📺🙍🏻‍♀️ Реклама Ж', callback_data='admin_setings_adv_f')
    admin_setings_adv_number = InlineKeyboardButton(text='📺 Частота рекламы', callback_data='admin_setings_adv_number')
    # admin_setings_fake_number = InlineKeyboardButton(text='🌠Частота фэйковых анкет',
    #                                                  callback_data='admin_settings_fake_number')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(admin_setings_adv_m)
    start_kb.add(admin_setings_adv_f)
    start_kb.add(admin_setings_adv_number)
    # start_kb.add(admin_setings_fake_number)
    start_kb.add(back)
    return start_kb


def admins_settings_adv_chat():
    status = int(read_by_name(table='constants', name='chat_roll_adv', id_name='id', id_data=1)[0][0])
    admin_setings_adv_m = InlineKeyboardButton(text='📺🙎‍♂️ Реклама М', callback_data='admin_setings_adv_m')
    admin_setings_adv_f = InlineKeyboardButton(text='📺🙍🏻‍♀️ Реклама Ж', callback_data='admin_setings_adv_f')
    if status == 0:
        admin_setings_adv_number = InlineKeyboardButton(text='📺 Включить ✅', callback_data='admin_setings_chat_adv_on')
    else:
        admin_setings_adv_number = InlineKeyboardButton(text='📺 Отключить ❌', callback_data='admin_setings_chat_adv_off')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup().add(admin_setings_adv_m)
    start_kb.add(admin_setings_adv_f)
    start_kb.add(admin_setings_adv_number)
    # start_kb.add(admin_setings_fake_number)
    start_kb.add(back)
    return start_kb


def admins_fake_people():
    status = int(read_by_name(table='constants', name='fake_post', id_name='id', id_data=1)[0][0])
    admin_setings_adv_f = InlineKeyboardButton(text='🤖🙍🏻‍♀️ Боты Просмотр 🙎‍♂️', callback_data='admin_bot_work')
    new_bot = InlineKeyboardButton(text='🤖🙍 Новый бот', callback_data='new_bot')
    if status == 0:
        admin_setings_adv_number = InlineKeyboardButton(text='🤖 Включить боты ✅', callback_data='admin_bot_on')
    else:
        admin_setings_adv_number = InlineKeyboardButton(text='🤖 Отключить боты ❌', callback_data='admin_bot_off')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(admin_setings_adv_f)
    start_kb.add(new_bot)
    start_kb.add(admin_setings_adv_number)
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


def remove_adv(adv: tuple):
    user_main = InlineKeyboardMarkup()
    for ad in adv:
        back = InlineKeyboardButton(text=f"❌ {ad[1]}", callback_data=f'delete_ad_{ad[0]}')
        user_main.add(back)
    return user_main


def admin_bots(bots: tuple):
    user_main = InlineKeyboardMarkup()
    for bot in bots:
        bot_data = join_get_bot(bot[1])[0]
        back = InlineKeyboardButton(text=f"{bot_data[0]},{bot_data[1]},{bot_data[2]},{bot_data[3]},{bot_data[4]}",
                                    callback_data=f'admin_bot_{bot[1]}')
        user_main.add(back)
    return user_main


# клавиатура для админа стартовая
def confirm(without_back=False, without_yes=False):
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
    send_en = InlineKeyboardButton(text=f'Все 🇬🇧', callback_data=f'send_en')
    send_ru = InlineKeyboardButton(text=f'Все 🇷🇺', callback_data=f'send_ru')
    send_boys = InlineKeyboardButton(text=f'Все парни', callback_data=f'send_boys')
    send_girls = InlineKeyboardButton(text=f'Все девушки', callback_data=f'send_girls')
    send_age = InlineKeyboardButton(text=f'Всем по возрасту', callback_data=f'send_age')
    send_city = InlineKeyboardButton(text=f'Всем в Городе', callback_data=f'send_city')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    user_main.add(send_all)
    user_main.add(send_ru, send_en)
    user_main.add(send_boys, send_girls)
    user_main.add(send_age)
    user_main.add(send_city)
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
