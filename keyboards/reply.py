from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_main() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Income')
    builder.button(text='Expense')
    builder.button(text='Transfer')
    builder.button(text='Settings')

    return builder.as_markup(resize_keyboard=True)