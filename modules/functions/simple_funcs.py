
from modules.sql_func import update_db


def update_age_period(tg_ig: int, age: int):
    if 16 <= age <= 18:
        update_db(table='fast_info', name='age_min', data=16, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=18, id_data=tg_ig)
    elif 18 <= age <= 24:
        update_db(table='fast_info', name='age_min', data=18, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=24, id_data=tg_ig)
    elif 24 <= age <= 29:
        update_db(table='fast_info', name='age_min', data=24, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=30, id_data=tg_ig)
    elif 30 <= age <= 35:
        update_db(table='fast_info', name='age_min', data=30, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=35, id_data=tg_ig)
    elif 36 <= age <= 45:
        update_db(table='fast_info', name='age_min', data=36, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=45, id_data=tg_ig)
    elif 46 <= age <= 60:
        update_db(table='fast_info', name='age_min', data=46, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=60, id_data=tg_ig)
    elif 60 <= age <= 80:
        update_db(table='fast_info', name='age_min', data=60, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=80, id_data=tg_ig)
    elif 80 <= age <= 120:
        update_db(table='fast_info', name='age_min', data=80, id_data=tg_ig)
        update_db(table='fast_info', name='age_max', data=120, id_data=tg_ig)
