from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text

from modules.keyboards import compotibility_kb


# Start menu
@dp.message_handler(Text(equals='❤️‍🔥 Совместимость', ignore_case=True), state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных
    await message.answer(text='Любовь с первого взгляда, бабочки в животе и головокружение - все это, конечно, '
                              'романтично и прекрасно.\n'
                              'Однако, только на первых порах. Затем могут последовать сложные ситуации, выход из '
                              'которых вам придется искать вместе.\n'
                              'Исходя из этого мы разработали специальный тест на основе нумерологии, гороскопа, '
                              'интересах и пр., который поможет узнать совместимость с вашей второй половинкой, '
                              'и расскажем по подробнее над чем вам придется работать в отношениях.',
                         reply_markup=compotibility_kb())
