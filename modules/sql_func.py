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
             user_age BIGINT,
             user_sex TEXT,
             city TEXT,
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
             fast_3 TEXT DEFAULT '0')''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Админ создает таблицу для рассылки
def sender_table():
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS sender (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             text TEXT DEFAULT '0',
             media_type TEXT DEFAULT '0',
             media_id TEXT DEFAULT '0',
             k_board TEXT DEFAULT '0'
             )''')
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


# Добавляем данные новому пользователю
def insert_user(name: str, tg_id: str, table: str = 'all_users'):
    global data_base
    data_now = datetime.datetime.now()
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, user_name, first_reg, activity) "
                           f"VALUES (%s, %s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, name, data_now, data_now))
            data_base.commit()
            cursor.execute(f"INSERT INTO fast_info (tg_id) "
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


# Обновляем данные в базе данных
def update_db(data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET {name}=(%s) WHERE {id_name}=(%s)", (data, id_data))
            data_base.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)


# Обновляем данные в базе данных
def grow_balls_db(data, id_name: str = 'tg_id'):
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"UPDATE fast_info SET balls_balance = balls_balance + 50 WHERE {id_name}=(%s)", (data, ))
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


# Собираем все записи с фильтрацией по 1 параметру
def read_by_name(
        id_data,
        id_name: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    global data_base
    try:
        with data_base.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}='{id_data}'")
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


# Удаляем строку в таблице
def delete_line_in_table(data, table: str = 'all_categorys', name: str = 'id'):
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
