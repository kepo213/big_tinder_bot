import datetime

import requests
from modules.setings import MainSettings
from modules.sql_func import data_base, read_all, search_person_smart_sender

settings = MainSettings()
tg_token = settings.tg_token()

API_link = f'https://api.telegram.org/bot{tg_token}/'


def search_users(smart_post: tuple):
    post_type = smart_post[5]
    if post_type == 'lust_active':
        search_key = 'activity'
    elif post_type == 'lust_active':
        search_key = 'first_reg'
    else:
        return
    lust_check = smart_post[8]
    time_delta = smart_post[4]
    search_sex = smart_post[6]
    time_now = datetime.datetime.now() - datetime.timedelta(days=time_delta)
    find_all_persons = search_person_smart_sender(search_key=search_key,
                                                  lust_seach=lust_check,
                                                  time_now=time_now,
                                                  search_sex=search_sex)
    return time_now


def start_sender():
    while True:
        all_smart_posts = read_all(table='smart_sender')
        for smart_post in all_smart_posts:
            time_now = search_users(smart_post=smart_post)
        lust_check = datetime.datetime.now()


if __name__ == '__main__':
    try:
        start_sender()
    except Exception as _ex:
        print(_ex)
    finally:
        data_base.close()
