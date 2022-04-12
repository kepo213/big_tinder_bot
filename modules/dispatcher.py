from aiogram import Bot, Dispatcher
from modules.setings import MainSettings
from modules.filters import NotAllProfile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

constant = MainSettings()
telegram_token = constant.tg_token()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(telegram_token)
dp = Dispatcher(bot, storage=storage)

# Включаем фильтры
dp.filters_factory.bind(NotAllProfile)


class Admin(StatesGroup):
    start = State()


class AdminSettings(StatesGroup):
    start = State()
    adv_number = State()


class Admin_sender(StatesGroup):
    new_text_post = State()
    new_media = State()
    new_k_board = State()
    choose_users = State()
    confirm_sender = State()


class User(StatesGroup):
    start = State()
    set_name = State()
    set_age = State()
    set_sex = State()
    set_geo = State()
    set_geo_confirm = State()
    set_photo = State()


class UserSettings(StatesGroup):
    start = State()
    range_period = State()
    language = State()

    age_period = State()
    age_period_max = State()


class UserProfile(StatesGroup):
    start = State()
    name = State()
    age = State()

    sex = State()
    city = State()
    photo = State()

    about = State()
    emoji = State()
    zodiac = State()

    Instagram = State()
    verification = State()

class UserPremium(StatesGroup):
    start = State()
