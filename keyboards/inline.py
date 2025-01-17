from typing import List

from dao.models import Category
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_main() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Income', callback_data='income')
    builder.button(text='Expense', callback_data='expense')
    builder.button(text='Transfer', callback_data='transfer')
    builder.button(text='Settings', callback_data='settings')
    builder.adjust(1)

    return builder.as_markup()


def ikb_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Categories', callback_data='settings_categories')
    builder.button(text='Accounts', callback_data='settings_accounts')
    # builder.button(text='', callback_data='')
    # builder.button(text='', callback_data='')
    builder.button(text='Back', callback_data='main')
    # builder.button(text='', callback_data='')
    # builder.button(text='', callback_data='')
    # builder.button(text='', callback_data='')
    builder.adjust(1)

    return builder.as_markup()


def ikb_settings_categories(categories_data: List[Category]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in categories_data:
        builder.button(text=category.name, callback_data=f'category_{category.id}')
    builder.button(text='Add new category', callback_data='add_new_category')
    builder.button(text='Back', callback_data='settings')
    builder.adjust(1)

    return builder.as_markup()


def ikb_income_expense() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Income', callback_data='add_category_income')
    builder.button(text='Expense', callback_data='add_category_expense')
    builder.button(text='Back', callback_data='settings_categories')
    builder.adjust(1)

    return builder.as_markup()


def ikb_edit_category(category_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Edit name', callback_data=f'edit_category_name_{category_id}')
    builder.button(text='Edit type', callback_data=f'edit_category_type_{category_id}')
    builder.button(text='Delete category', callback_data=f'delete_category_{category_id}')
    builder.button(text='Back', callback_data=f'settings_categories')
    builder.adjust(1)

    return builder.as_markup()
