from aiogram import Bot, Dispatcher
from modules.setings import MainSettings
from modules.filters import NotAllProfile, CheckActivity, CheckActivityCall, InChatRoll, PremiumInChatRoll
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
dp.filters_factory.bind(CheckActivity)
dp.filters_factory.bind(CheckActivityCall)
dp.filters_factory.bind(InChatRoll)
dp.filters_factory.bind(PremiumInChatRoll)


class Admin(StatesGroup):
    start = State()


class AdminSettings(StatesGroup):
    start = State()
    adv_start = State()
    adv_number = State()
    fake_post_number = State()

    adv_text = State()
    adv_url = State()
    adv_photo = State()
    adv_confirm = State()

    chat_roll_adv = State()
    chat_roll_add_adv = State()


class AdminSender(StatesGroup):
    new_text_post = State()
    new_media = State()
    new_k_board = State()
    choose_users = State()
    confirm_sender = State()

    sender_min_age = State()
    sender_max_age = State()
    sender_confirm = State()

    sender_city = State()
    sender_city_confirm = State()


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


class UserCouples(StatesGroup):
    start = State()


class UserLikes(StatesGroup):
    start = State()
    check_inform = State()


class UserChatRoll(StatesGroup):
    start = State()
    talk = State()

    score = State()
    settings = State()
