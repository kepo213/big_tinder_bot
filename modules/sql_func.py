import datetime

import psycopg2
from modules.setings import MainSettings

constant = MainSettings()

data_base = psycopg2.connect(
    host=constant.db_host(),
    user=constant.user_db(),
    password=constant.password_db(),
    database=constant.db_name())


# Новый юзер создает таблицу в бд
def all_users_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             user_name TEXT,
             status TEXT DEFAULT 'need_reg',
             language TEXT DEFAULT 'ru',
             first_reg timestamp,
             activity timestamp)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def photo_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS gallery (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             media_id TEXT,
             media_type TEXT,
             status TEXT DEFAULT 'active')''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def create_fast_info_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS fast_info (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             user_nickname TEXT DEFAULT '0',
             user_age BIGINT DEFAULT 18,
             user_sex TEXT DEFAULT 'female',
             search_sex TEXT DEFAULT 'all',
             city TEXT DEFAULT 'Москва',
             longitude DOUBLE PRECISION,
             latitude DOUBLE PRECISION,
             photo_id TEXT DEFAULT '0',
             photo_good TEXT DEFAULT '0',
             about_text TEXT DEFAULT '0',
             emoji TEXT DEFAULT '0',
             zodiac TEXT DEFAULT '0',
             instagram TEXT DEFAULT '0',
             premium TEXT DEFAULT '0',
             search_range BIGINT DEFAULT 300,
             search_status INTEGER DEFAULT 1,
             age_min BIGINT DEFAULT 18,
             age_max BIGINT DEFAULT 24,
             balls_balance BIGINT DEFAULT 100,
             fast_1 TEXT DEFAULT '0',
             fast_2 TEXT DEFAULT '0',
             fast_3 TEXT DEFAULT '0',
             fast_4 TEXT DEFAULT '0',
             fast_5 TEXT DEFAULT '0')''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def for_couples_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS couples (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             lust_couple_id BIGINT DEFAULT 0,
             adv BIGINT DEFAULT 0)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def likes_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS likes (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT,
             from_tg_id BIGINT DEFAULT 0,
             status_from TEXT DEFAULT 'no',
             status_to TEXT DEFAULT 'no')''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def chat_roll_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS chat_roll (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT,
             status INTEGER DEFAULT 0,
             messages INTEGER DEFAULT 0,
             chats INTEGER DEFAULT 0,
             karma INTEGER DEFAULT 0,
             friend_id BIGINT DEFAULT 0,
             lust_adv BIGINT DEFAULT 0)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Новый юзер создает таблицу в бд
def presents_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS presents (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT,
             from_tg_id BIGINT DEFAULT 0,         
             status_from TEXT DEFAULT 'no',
             status_to TEXT DEFAULT 'no')''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def constants_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS constants (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             text TEXT DEFAULT '0',
             media_type TEXT DEFAULT '0',
             media_id TEXT DEFAULT '0',
             k_board TEXT DEFAULT '0',
             adv_number BIGINT DEFAULT 6,
             fake_post BIGINT DEFAULT 1,
             chat_roll_adv BIGINT DEFAULT 1
             )''')
            data_base.commit()
            cursor.execute(f"INSERT INTO constants (id) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (1,))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def reffs_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS reff (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             mentor_tg_id BIGINT DEFAULT '0',
             date timestamp
             )''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def smart_sender():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS smart_sender (
             id SERIAL PRIMARY KEY,
             text TEXT DEFAULT '0',
             btn_name TEXT DEFAULT '0',
             btn_url TEXT DEFAULT '0',
             days BIGINT DEFAULT 0,
             type TEXT DEFAULT '0',
             sex TEXT DEFAULT 'men',
             photo_id TEXT DEFAULT '0',
             lust_check timestamp
             )''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def bots_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS bots (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def adv_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS adv (
             id SERIAL PRIMARY KEY,
             users_sex TEXT DEFAULT '0',
             text TEXT DEFAULT '0',
             photo_id TEXT DEFAULT '0',
             btn_url TEXT DEFAULT '0'
             )''')
            data_base.commit()
            cursor.execute(f"INSERT INTO adv (id, users_sex) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (1, 'men'))
            data_base.commit()
            cursor.execute(f"INSERT INTO adv (id, users_sex) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (2, 'female'))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def chat_adv_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS chat_adv (
             id SERIAL PRIMARY KEY,
             users_sex TEXT DEFAULT '0',
             text TEXT DEFAULT '0',
             photo_id TEXT DEFAULT '0',
             btn_url TEXT DEFAULT '0'
             )''')
            data_base.commit()
            cursor.execute(f"INSERT INTO adv (id, users_sex) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (1, 'men'))
            data_base.commit()
            cursor.execute(f"INSERT INTO adv (id, users_sex) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (2, 'female'))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные новому пользователю
def insert_user(name: str, tg_id: str, user_nickname: str, table: str = 'all_users'):
    global data_base
    data_now = datetime.datetime.now()
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, user_name, first_reg, activity) "
                           f"VALUES (%s, %s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, name, data_now, data_now))
            data_base.commit()
            cursor.execute(f"INSERT INTO fast_info (tg_id, user_nickname) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, user_nickname))
            data_base.commit()
            cursor.execute(f"INSERT INTO couples (tg_id) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id,))
            data_base.commit()
            cursor.execute(f"INSERT INTO chat_roll (tg_id) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id,))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные новому пользователю
def reff_user(tg_id: str, mentor_tg_id: str):
    global data_base
    data_now = datetime.datetime.now()
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO reff (tg_id, mentor_tg_id, date) "
                           f"VALUES (%s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, mentor_tg_id, data_now))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные новому пользователю
def new_adv(sex: str, text: str):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO chat_adv (users_sex, text) "
                           f"VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (sex, text))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные новому пользователю
def insert_first(table: str, name: str, data):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} ({name}) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (data,))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные новому пользователю
def new_smart_sener(text: str, btn_name: str, btn_url: str, days: int, post_type: str, sex: str, photo_id: str):
    global data_base
    try:
        lust_date = datetime.datetime.now()
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO smart_sender (text, btn_name, btn_url, days, type, sex, photo_id, lust_check) "
                           f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (text, btn_name, btn_url, days, post_type, sex, photo_id, lust_date))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем данные по соннику
def insert_in_db(name: str, tg_id: str, data: str, table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, {name}) VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, data))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Добавляем лайк
def insert_likes_presents_db(tg_id: int, from_tg_id: int, table: str = 'likes'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, from_tg_id, status_from) VALUES (%s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, from_tg_id, 'active'))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def update_db(data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET {name}=(%s) WHERE {id_name}=(%s)", (data, id_data))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def update_city_db(data, latitude: str, longitude: str, id_data, id_name: str = 'tg_id'):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE fast_info SET city=(%s), latitude=(%s), longitude=(%s)  WHERE {id_name}=(%s)",
                           (data, latitude, longitude, id_data))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def update_adv_db(text: str, photo_id: str, btn_url: str, id_data: int):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE adv SET text=(%s), photo_id=(%s), btn_url=(%s)  WHERE id=(%s)",
                           (text, photo_id, btn_url, id_data))
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def grow_balls_db(data, id_name: str = 'tg_id'):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE fast_info SET balls_balance = balls_balance + 50 WHERE {id_name}=(%s)", (data,))
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def grow_chat_messages_db(tg_id: int):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE chat_roll SET messages = messages + 1 WHERE tg_id=(%s)", (tg_id,))
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def grow_chat_chats_db(tg_id: int):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE chat_roll SET chats = chats + 1 WHERE tg_id=(%s)", (tg_id,))
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def grow_chat_karma_db(score: int, tg_id: int):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE chat_roll SET karma = karma + (%s) WHERE tg_id=(%s)", (score, tg_id))
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Читаем все данные из базы данных
def read_all(
        name: str = '*',
        table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'SELECT {name} FROM {table}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Читаем все данные из базы данных
def read_all_order(
        name: str = '*',
        table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'SELECT {name} FROM {table} ORDER BY id DESC')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Читаем все данные из базы данных
def chat_score_join(key: str = '*'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'SELECT chat_roll.tg_id, all_users.user_name, chat_roll.{key} FROM chat_roll '
                           f'INNER JOIN all_users ON chat_roll.tg_id = all_users.tg_id ORDER BY chat_roll.{key} DESC LIMIT 10')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Читаем все данные из базы данных
def count_all(
        table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Читаем все данные из базы данных
def count_refs_for_chats(tg_id: int,
                         table: str = 'reff'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM {table} WHERE mentor_tg_id = {tg_id}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def read_by_name(
        id_data,
        id_name: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    """
    :rtype: tuple
    """
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}='{id_data}'")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def read_adv(
        id_data,
        id_name: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    """
    :rtype: tuple
    """
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}='{id_data}' ORDER BY id DESC LIMIT 10")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def get_ad_by_sex(sex: str, lust_ad_id: int):
    """
    :rtype: tuple
    """
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT id, text FROM chat_adv WHERE users_sex = (%s) AND id > (%s)",
                           (sex, lust_ad_id))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def count_chats():
    """
    :rtype: tuple
    """
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM chat_roll WHERE (friend_id != 0 AND status = 0) OR "
                           f"(status = 1)")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def search_person(
        x_left: float, x_right: float,
        y_up: float, y_down: float, search_sex: str, lust_id: int,
        age_min: int, age_max: int, status: str):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT fast_info.id, all_users.tg_id, fast_info.photo_id FROM fast_info "
                           f"INNER JOIN all_users ON fast_info.tg_id = all_users.tg_id WHERE "
                           f"(fast_info.longitude BETWEEN '{x_left}' AND '{x_right}') "
                           f"AND (fast_info.latitude BETWEEN '{y_down}' AND '{y_up}') "
                           f"AND (fast_info.user_age BETWEEN '{age_min}' AND '{age_max}') "
                           f"AND (fast_info.id > {lust_id}) "
                           f"AND (fast_info.user_sex = '{search_sex}') "
                           f"AND (all_users.status = '{status}') "
                           f"AND (fast_info.search_status = 1) ORDER BY fast_info.id")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def search_person_smart_sender(search_key: str,
                               lust_seach: datetime.datetime, time_now: datetime.datetime,
                               search_sex: str, ):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, fast_info.user_sex FROM all_users "
                           f"INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id WHERE "
                           f"(fast_info.{search_key} BETWEEN '{lust_seach}' AND '{time_now}') "
                           f"AND (fast_info.user_sex = '{search_sex}') "
                           f"AND (all_users.status = 'active')")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 1 параметру
def search_persons_for_sender(
        x_left: float, x_right: float,
        y_up: float, y_down: float):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT fast_info.tg_id, all_users.status FROM fast_info INNER JOIN all_users ON "
                           f"fast_info.tg_id = all_users.tg_id WHERE "
                           f"(fast_info.longitude BETWEEN '{x_left}' AND '{x_right}') "
                           f"AND (fast_info.latitude BETWEEN '{y_down}' AND '{y_up}') "
                           f"AND (all_users.status = 'active')")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def read_all_by_date(days: int = 30,
                     data_column: str = 'first_reg'):
    global data_base
    try:
        data_now = datetime.datetime.now()
        data_30 = data_now - datetime.timedelta(days=days)
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT * FROM all_users WHERE {data_column} between "
                           f"'{data_30}'::timestamp and "
                           f"'{data_now}'::timestamp order by id desc")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def join_chat_data(tg_id: int):
    global data_base
    try:
        data_now = datetime.datetime.now()
        data_15 = data_now - datetime.timedelta(minutes=15)
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, chat_roll.status, fast_info.user_sex, all_users.activity FROM "
                           f"((all_users INNER JOIN chat_roll ON all_users.tg_id = chat_roll.tg_id) "
                           f"INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id) WHERE "
                           f"(all_users.activity BETWEEN "
                           f"'{data_15}'::timestamp AND "
                           f"'{data_now}'::timestamp) AND "
                           f"(chat_roll.status = 1) AND "
                           f"(chat_roll.karma > -10) AND "
                           f"(all_users.tg_id != (%s))", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def join_chat_data_sex(tg_id: int, sex: str):
    global data_base
    try:
        data_now = datetime.datetime.now()
        data_15 = data_now - datetime.timedelta(minutes=15)
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, chat_roll.status, fast_info.user_sex, all_users.activity FROM "
                           f"((all_users INNER JOIN chat_roll ON all_users.tg_id = chat_roll.tg_id) "
                           f"INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id) WHERE "
                           f"(all_users.activity BETWEEN "
                           f"'{data_15}'::timestamp AND "
                           f"'{data_now}'::timestamp) AND "
                           f"(chat_roll.status = 1) AND "
                           f"(chat_roll.karma > -10) AND "
                           f"(fast_info.user_sex = (%s)) AND "
                           f"(all_users.tg_id != (%s))", (sex, tg_id))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def join_get_bot(tg_id: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, all_users.user_name, fast_info.user_sex, fast_info.user_age, "
                           f"fast_info.city FROM "
                           f"all_users INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id "
                           f"WHERE all_users.tg_id = (%s)", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def join_sender_sex(sex: str):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, all_users.status, fast_info.user_sex FROM "
                           f"all_users INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id "
                           f"WHERE all_users.status = 'active' AND "
                           f"fast_info.user_sex = (%s)", (sex,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по интервалу дат
def join_sender_age(age_min: int, age_max: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, fast_info.user_age FROM "
                           f"all_users INNER JOIN fast_info ON all_users.tg_id = fast_info.tg_id "
                           f"WHERE all_users.status = 'active' AND "
                           f"fast_info.user_age BETWEEN (%s) AND (%s)", (age_min, age_max))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def read_all_2(
        id_data,
        id_data2,
        id_name: str = 'tg_id',
        id_name2: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}=(%s) AND {id_name2}=(%s)", (id_data, id_data2))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def read_all_3(
        id_data,
        id_data2,
        id_data3,
        id_name: str = 'tg_id',
        id_name2: str = 'tg_id',
        id_name3: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    '''
    :rtype :tuple
    '''
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}=(%s) AND {id_name2}=(%s) AND {id_name3}=(%s)",
                           (id_data, id_data2, id_data3))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_likes(tg_id: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, all_users.user_name, fast_info.user_age, fast_info.city "
                           f"FROM all_users JOIN fast_info ON all_users.tg_id = fast_info.tg_id WHERE "
                           f"all_users.tg_id = (%s)", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_help_all(id_data: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, all_users.user_name, all_users.language, fast_info.user_age, "
                           f"fast_info.city, fast_info.photo_id "
                           f"FROM all_users JOIN fast_info ON all_users.tg_id = fast_info.tg_id WHERE "
                           f"all_users.tg_id=(%s)", (id_data,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_reff_block(tg_id: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT reff.tg_id, reff.mentor_tg_id, all_users.status "
                           f"FROM reff JOIN all_users ON reff.tg_id = all_users.tg_id WHERE "
                           f"reff.mentor_tg_id = (%s) AND all_users.status = 'close'", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_reff_premium(tg_id: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT reff.tg_id, reff.mentor_tg_id, fast_info.premium "
                           f"FROM reff JOIN fast_info ON reff.tg_id = fast_info.tg_id WHERE "
                           f"reff.mentor_tg_id = (%s) AND fast_info.premium = '1'", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_reff_photo(tg_id: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT reff.tg_id, reff.mentor_tg_id, fast_info.photo_id "
                           f"FROM reff JOIN fast_info ON reff.tg_id = fast_info.tg_id WHERE "
                           f"reff.mentor_tg_id = (%s) AND fast_info.photo_id = '0'", (tg_id,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_profile_all(id_data: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.tg_id, all_users.user_name, fast_info.user_age, fast_info.city,"
                           f"fast_info.photo_id, fast_info.photo_good, fast_info.about_text, fast_info.emoji,"
                           f"fast_info.zodiac, fast_info.instagram, fast_info.premium "
                           f"FROM all_users JOIN fast_info ON all_users.tg_id = fast_info.tg_id WHERE "
                           f"all_users.tg_id=(%s)", (id_data,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Собираем все записи с фильтрацией по 3 параметрам
def join_chat_stata(id_data: int):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT all_users.user_name, fast_info.user_sex, fast_info.age_min, fast_info.age_max, "
                           f"fast_info.city FROM all_users JOIN fast_info ON all_users.tg_id = fast_info.tg_id WHERE "
                           f"all_users.tg_id=(%s)", (id_data,))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Удаляем строку в таблице
def delete_line_in_table(data, table: str = 'chat_adv', name: str = 'id'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table} WHERE {name}='{data}'")
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Удаляем таблицу
def delete_table(table: str):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
