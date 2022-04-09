from aiogram import executor
from modules.sql_func import data_base
from modules.dispatcher import dp


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as _ex:
        print(_ex)
    finally:
        print('Connection closet')
        data_base.close()
