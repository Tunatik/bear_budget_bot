from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def actions_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Income')
    builder.button(text='Expenses')
    builder.button(text='Accounts')
    builder.button(text='Settings')

    return builder.as_markup(resize_keyboard=True)
