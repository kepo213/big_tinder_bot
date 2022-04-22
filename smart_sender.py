import datetime
import json
import time

import requests
from modules.setings import MainSettings
from modules.sql_func import data_base, read_all, search_person_smart_sender, update_db

settings = MainSettings()
tg_token = settings.tg_token()

API_link = f'https://api.telegram.org/bot{tg_token}/'


def send_text_post(user_id: int, text: str, k_board_name: str, k_board_url: str):
    if k_board_name == '0':
        req_text = API_link + f'sendMessage?chat_id={user_id}&text={text}&parse_mode=html'
    else:
        k_board = {"inline_keyboard": [[{'text': k_board_name, 'url': k_board_url}]]}
        req_text = API_link + f'sendMessage?chat_id={user_id}&text={text}&parse_mode=html&reply_markup={json.dumps(k_board)}'
    try:
        ans = requests.post(url=req_text)
        # print(ans.json())
        status = ans.json()['ok']
        if not status:
            update_db(table="all_users", name="status", data="close", id_data=user_id)
    except:
        pass


def send_photo_post(user_id: int, text: str, k_board_name: str, k_board_url: str, photo_id: str):
    if k_board_name == '0':
        req_text = API_link + f'sendPhoto?chat_id={user_id}&caption={text}&parse_mode=html&photo={photo_id}'
    else:
        k_board = {"inline_keyboard": [[{'text': k_board_name, 'url': k_board_url}]]}
        req_text = API_link + f'sendPhoto?chat_id={user_id}&caption={text}&parse_mode=html&reply_markup={json.dumps(k_board)}&photo={photo_id}'
    try:
        ans = requests.post(url=req_text)
        # print(ans.json())
        status = ans.json()['ok']
        if not status:
            update_db(table="all_users", name="status", data="close", id_data=user_id)
    except:
        pass


def search_users(smart_post: tuple):
    post_type = str(smart_post[5])
    if post_type == 'lust_active':
        search_key = 'activity'
    elif post_type == 'first_reg':
        search_key = 'first_reg'
    else:
        return
    time_delta = smart_post[4]
    lust_check = smart_post[8] - datetime.timedelta(hours=time_delta)
    search_sex = smart_post[6]
    time_now = datetime.datetime.now()
    find_all_persons = search_person_smart_sender(search_key=search_key,
                                                  lust_seach=lust_check,
                                                  time_now=time_now - datetime.timedelta(hours=time_delta),
                                                  search_sex=search_sex)
    update_db(table='smart_sender', name='lust_check', data=time_now, id_name='id', id_data=smart_post[0])
    if smart_post[7] == '0':
        for user in find_all_persons:
            send_text_post(user_id=user[0], text=smart_post[1], k_board_name=smart_post[2], k_board_url=smart_post[3])
    else:
        pass
        for user in find_all_persons:
            send_photo_post(user_id=user[0], text=smart_post[1], k_board_name=smart_post[2], k_board_url=smart_post[3], photo_id=smart_post[7])
    return


def start_sender():
    while True:
        all_smart_posts = read_all(table='smart_sender')
        for smart_post in all_smart_posts:
            search_users(smart_post=smart_post)
        time.sleep(10)


if __name__ == '__main__':
    try:
        start_sender()
    except Exception as _ex:
        print(_ex)
    finally:
        data_base.close()
