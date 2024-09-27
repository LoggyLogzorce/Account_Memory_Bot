import asyncio
import logging
import os

import psycopg2

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile

from config import TOKEN
from keyboard import ReplyMarkup, deleteMarkup, deleteInlineMarkup, all_title_Markup, updateMarkup, confirmation

from db import (data_output_title, entering_data, entering_data_temporary, full_delete_data, data_output, update_data,
                delete_data, delete_temporary, add_polzovatel)
from titulnik import titulnik

connection = psycopg2.connect(user="postgres",
                              password="1234",
                              host="127.0.0.1",
                              port="5432",
                              database='BotMemory')

cursor = connection.cursor()


async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я запомню данные твоих учётных записей.'
                         f'\nЯ буду твоим помощником и буду выдавать твои данные от учётных записей, '
                         f'но для начала нужно их добавить.'
                         f'\n\nНажми на кнопку добавить.', reply_markup=ReplyMarkup)

    add_polzovatel(cursor, message.from_user.username)
    connection.commit()


async def add_await(message: types.Message):
    await message.answer(f'Введи название и данные учётной записи. \nНапример: \nMicrosoft Login Password\n\nили \n\n'
                         f'Microsoft \nLogin \nPassword')


async def my_acc(message: types.Message):
    row = data_output(cursor, message.from_user.username)

    if not row:
        await message.answer('У вас пока нет записей', reply_markup=ReplyMarkup)
    else:
        await message.answer('Ваши записи ⬇️', reply_markup=all_title_Markup(cursor, str(message.from_user.username)))

    connection.commit()


async def delete_acc(message: types.Message):
    row = data_output(cursor, message.from_user.username)

    if not row:
        await message.answer('У вас пока нет записей', reply_markup=ReplyMarkup)
    else:
        await message.answer('Нашёл ваши записи, что сделать?', reply_markup=deleteMarkup)

    connection.commit()


async def one_delete_acc(message: types.Message):
    await message.answer(f'Какую запись удалить?',
                         reply_markup=deleteInlineMarkup(cursor, str(message.from_user.username)))


async def full_delete_acc(message: types.Message):
    row = data_output(cursor, message.from_user.username)

    if row is None:
        await message.answer('У вас пока нет записей', reply_markup=ReplyMarkup)
    else:
        await message.answer(f'Вы действительно хотите удалить все записи?', reply_markup=confirmation())


async def add_output(message: types.Message, bot: Bot):
    if len(message.text.split()) == 1:
        row = data_output_title(cursor, message.from_user.username, message.text)

        if row is None:
            await message.reply(f'🤷‍♀️ Записи с данным названием не найдено.\nПроверьте правильность написания.')
        else:
            await message.answer(f'Данные записи: {row[2]}\n\nЛогин: `{row[3]}`\n\nПароль: `{row[4]}`',
                                 parse_mode="MARKDOWN")

    elif len(message.text.split()) == 3:
        title = message.text.split()[0]
        login = message.text.split()[1]
        password = message.text.split()[2]

        update = data_output_title(cursor, message.from_user.username, title)

        if update is None:
            entering_data(cursor, message.from_user.username, title, login, password)
            await message.reply('✅ Запись добавлена! \nЧтобы вывести данные напишите название.',
                                reply_markup=ReplyMarkup)

            connection.commit()
        else:
            await message.reply(f'❌ Запись с названием {title} уже существует\n'
                                f'Если требуется добавить эту запись, то измените название',
                                reply_markup=updateMarkup())
            delete_temporary(cursor, message.from_user.username)
            entering_data_temporary(cursor, message.from_user.username, title, login, password)

            connection.commit()

    elif len(message.text.split('\n')) == 5:
        await message.reply('Титульник в процессе создания', reply_markup=ReplyMarkup)
        title = titulnik(message.text)
        document = FSInputFile(f'{title}')
        await bot.send_document(message.chat.id, document)
        os.remove(f"{title}")

    else:
        await message.reply('❌ Неправильное введение данных. \nПроверьте количество пробелов и повторите попытку.')


async def Callback(callback_query: CallbackQuery):
    if callback_query.data == 'updateData':
        update_data(cursor, callback_query.from_user.username)

        await callback_query.message.answer(f'✅ Запись обновлена!', reply_markup=ReplyMarkup)

    elif callback_query.data == 'confirmation_yes':
        full_delete_data(cursor, callback_query.from_user.username)

        await callback_query.message.answer(f'✅ Все ваши записи удалены!', reply_markup=ReplyMarkup)

    elif callback_query.data == 'confirmation_no':
        await callback_query.message.answer(f'Все ваши записи остаются', reply_markup=ReplyMarkup)

    else:
        delete_data(cursor, callback_query.from_user.username, callback_query.data.split()[1])

        await callback_query.message.answer(f'✅ Запись удалена: {callback_query.data.split()[1]}',
                                            reply_markup=ReplyMarkup)

    connection.commit()


async def menu(message: types.Message):
    await message.answer('Выберите команду', reply_markup=ReplyMarkup)


async def start_titulnik(message: types.Message):
    await message.answer('Для созданния титульника введите необходимые данные😒')
    await message.answer('ФИО студента\nГруппу\nПреподавателя\nКак называется дисциплина\n'
                         'Название лабораторной\n\nДанные должны быть написаны на новой строчке🫡',
                         reply_markup=ReplyMarkup)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(start, CommandStart())
    dp.message.register(add_await, F.text == 'Добавить')
    dp.message.register(my_acc, F.text == 'Все мои записи')
    dp.message.register(delete_acc, F.text == 'Удаление записей')
    dp.message.register(one_delete_acc, F.text == 'Удалить одну')
    dp.message.register(full_delete_acc, F.text == 'Удалить все записи')
    dp.message.register(menu, F.text == 'Назад')

    dp.message.register(start_titulnik, F.text == 'Создать титульник')

    dp.message.register(add_output)

    dp.callback_query.register(Callback)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


asyncio.run(main())
