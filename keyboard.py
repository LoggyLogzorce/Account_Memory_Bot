from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import data_output
from shifr import decrypt_data

ReplyMarkup = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Добавить"),
            types.KeyboardButton(text="Создать титульник")
        ],
        [
            types.KeyboardButton(text="Все мои записи"),
            types.KeyboardButton(text="Удаление записей")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Выбрать команду"
)

deleteMarkup = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Удалить одну"),
            types.KeyboardButton(text="Удалить все записи")
        ],
        [
            types.KeyboardButton(text="Назад")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder="Выбрать команду"
)


def deleteInlineMarkup(cursor, username):
    row = data_output(cursor, username)
    data_from_db = decrypt_data(row)
    builder = InlineKeyboardBuilder()
    for i in range(len(data_from_db)):
        builder.add(types.InlineKeyboardButton(text=f'{data_from_db[i][2]}', callback_data=f'button {data_from_db[i][2]}'))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def updateMarkup():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=f'Обновить данные 🆙', callback_data=f'updateData'))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def all_title_Markup(cursor, username):
    row = data_output(cursor, username)
    data_from_db = decrypt_data(row)

    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Назад'))
    for i in range(len(data_from_db)):
        builder.add(types.KeyboardButton(text=f'{data_from_db[i][2]}'))
    builder.adjust(1, 2)

    return builder.as_markup(resize_keyboard=True)


def confirmation():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=f'Да ✅', callback_data=f'confirmation_yes'))
    builder.add(types.InlineKeyboardButton(text=f'Нет ❌', callback_data=f'confirmation_no'))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
