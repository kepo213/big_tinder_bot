from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text

from modules.sql_func import join_help_all


def not_all_reg_data_text(tg_ig: int):
    user_data = join_help_all(id_data=tg_ig)
    text_data = {'name': '❌',
                 'age': '❌',
                 'city': '❌',
                 'photo': '❌'}
    if str(user_data) == '[]':
        pass
    if str(user_data[0][1]) != "None":
        text_data["name"] = '✅'
    if str(user_data[0][3]) != "None":
        text_data["age"] = '✅'
    if str(user_data[0][4]) != "None":
        text_data["city"] = '✅'
    if str(user_data[0][5]) != "0":
        text_data["photo"] = '✅'
    text = f'Эта команда будет доступна, после того как вы заполните в профиле следующие данные:\n' \
           f'Имя {text_data["name"]}\n' \
           f'Возраст {text_data["age"]}\n' \
           f'Город {text_data["city"]}\n' \
           f'Фото {text_data["photo"]}\n' \
           f'/start - Заполнить профиль с самого начала'
    return text


# Start menu
@dp.message_handler(commands=['info'], state='*')
@dp.message_handler(Text(equals='📌 Помощь', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных
    await message.answer(text='💜 MeetHub — is an online dating and geosocial networking bot. \n\n'
                              '❤️‍🔥 Бот для знакомств в Telegram, просто укажите свои данные и вы сможете знакомится с другими людьми.\n'
                              'Получать взаимные симпатии, подарки, а также провести анонимный диалог с незнакомцем.\n\n'
                              '🥰 Свайпай и лайкай других пользователей\n'
                              '🗺 Ищи новые знакомства в твоем городе\n'
                              '👀 Посмотри на парней и девушек которые находятся рядом\n'
                              '💬 Анонимная чат-рулетка\n\n'
                              '🎵┏ Подпишись на канал: @vkmusicbot1\n'
                              '📢┣ Прайс на рекламу: https://t.me/newchannel_media/14\n'
                              '🅰️┗ Если возникли сложности с ботом, пишите: @niktwix\n\n'
                              '🎥┏ Наш бот для поиска фильмов: @icinema_bot \n'
                              '💸┣ Как заработать  в  интернете @momsbiz \n'
                              '🎧┣ Бот для поиска музыки: @mixvk_bot \n'
                              '✍🏻┣ Красивые шрифты в Telegram: @Textsmakebot\n'
                              '🌎┣ Викторина по Географии: @natgeowild2\n'
                              '🍿┗ Канал о фильмах и сериалах: @ikinox')
