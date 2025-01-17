from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from utils.utils import delete_bot_message_with_delay, get_categories_from_telegram_id
from config import bot
from dao.dao import CategoryDAO
from dao.shemas import CategoryModel, CategoryIDModel, CategoryNameModel, CategoryTypeModel
from keyboards.inline import *


settings_router = Router()


class AddCategoryFSM(StatesGroup):
    type = State()
    name = State()


class EditCategoryFSM(StatesGroup):
    name = State()


@settings_router.callback_query(F.data == 'settings')
async def process_settings(call: CallbackQuery):
    await call.message.edit_text(
        text='Settings',
        reply_markup=ikb_settings()
    )

@settings_router.callback_query(F.data == 'settings_categories')
async def process_settings_categories(call: CallbackQuery, session_without_commit: AsyncSession):
    categories = await get_categories_from_telegram_id(telegram_id=call.from_user.id, session=session_without_commit)

    await call.message.edit_text(
        text='Your categories',
        reply_markup=ikb_settings_categories(categories)
    )

@settings_router.callback_query(F.data == 'add_new_category')
async def process_add_new_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(telegram_id=call.from_user.id)
    await state.set_state(AddCategoryFSM.type)
    await call.message.edit_text(
        text='Select type',
        reply_markup=ikb_income_expense()
    )

@settings_router.callback_query(F.data == 'add_category_income', AddCategoryFSM.type)
async def process_add_income_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(type='income', message_to_delete=call.message.message_id)
    await state.set_state(AddCategoryFSM.name)
    await call.message.edit_text(text='Enter name')

@settings_router.callback_query(F.data == 'add_category_expense', AddCategoryFSM.type)
async def process_add_expense_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(type='expense', message_to_delete=call.message.message_id)
    await state.set_state(AddCategoryFSM.name)
    await call.message.edit_text(text='Enter name')

@settings_router.message(F.text, AddCategoryFSM.name)
async def process_name_category(message: Message, state: FSMContext, session_with_commit: AsyncSession):
    categories = await get_categories_from_telegram_id(telegram_id=message.from_user.id, session=session_with_commit)
    data = await state.get_data()

    values = CategoryModel(
        name=message.text,
        type=data['type'],
        telegram_id=data['telegram_id']
    )

    await bot.delete_message(message.chat.id, message_id=data['message_to_delete'])
    await CategoryDAO.add(session=session_with_commit, values=values)
    await state.clear()
    bot_message = await message.answer(text='Successes')
    await delete_bot_message_with_delay(bot_message)
    await message.answer(
        text='Your categories',
        reply_markup=ikb_settings_categories(categories)
    )

@settings_router.callback_query(F.data.startswith('category_'))
async def process_edit_category(call: CallbackQuery, session_without_commit: AsyncSession):
    category_id = int(call.data.split('_')[-1])
    category = await CategoryDAO.find_one_or_none(session=session_without_commit, filters=CategoryIDModel(id=category_id))


    await call.message.edit_text(
        text=category.name,
        reply_markup=ikb_edit_category(category_id)
    )

@settings_router.callback_query(F.data.startswith('edit_category_name_'))
async def process_edit_category_name(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditCategoryFSM.name)
    await state.update_data(category_id=call.data.split('_')[-1])
    await call.message.edit_text(
        text='Enter new name for category'
    )

@settings_router.message(EditCategoryFSM.name)
async def process_edit_category_name_new(message: Message, session_with_commit: AsyncSession, state: FSMContext):
    data = await state.get_data()
    category_id = int(data['category_id'])
    values = CategoryNameModel(
        name=message.text
    )

    await CategoryDAO.update(session=session_with_commit, values=values, id=category_id)
    await state.clear()
    bot_message = await message.answer(
        text='Success'
    )
    await delete_bot_message_with_delay(bot_message)
    categories = await get_categories_from_telegram_id(telegram_id=message.from_user.id, session=session_with_commit)
    await message.answer(
        text='Your categories',
        reply_markup=ikb_settings_categories(categories)
    )

@settings_router.callback_query(F.data.startswith('edit_category_type_'))
async def process_edit_category_type(call: CallbackQuery, session_with_commit: AsyncSession):
    category_id = int(call.data.split('_')[-1])
    category_type = await CategoryDAO.find_one_or_none(session=session_with_commit, filters=CategoryIDModel(id=category_id))
    category_type = 'income' if category_type.type == 'expense' else 'expense'

    await CategoryDAO.update(session=session_with_commit, values=CategoryTypeModel(type=category_type), id=category_id)
    await call.answer(
        text=f'Category type changed to {category_type.title()}',
    )

@settings_router.callback_query(F.data.startswith('delete_category_'))
async def process_edit_category_delete(call: CallbackQuery, session_with_commit: AsyncSession):
    category_id = int(call.data.split('_')[-1])
    await CategoryDAO.delete(session=session_with_commit, id=category_id)
    bot_message = await call.message.edit_text(
        text='Success'
    )
    await delete_bot_message_with_delay(bot_message)
    categories = await get_categories_from_telegram_id(telegram_id=call.from_user.id, session=session_with_commit)
    await call.message.answer(
        text='Your categories',
        reply_markup=ikb_settings_categories(categories)
    )