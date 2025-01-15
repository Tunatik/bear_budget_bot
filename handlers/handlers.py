import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from config import bot
from dao.dao import UserDAO, CategoryDAO
from dao.models import User
from dao.shemas import TelegramIDModel, UserModel, CategoryModel
from keyboards.reply import *
from keyboards.inline import *


user_router = Router()


class IncomeExpenseFSM(StatesGroup):
    amount = State()


class AddCategoryFSM(StatesGroup):
    type = State()
    name = State()


@user_router.message(CommandStart())
async def process_cmd_start(message: Message, session_with_commit: AsyncSession):
    user_id = message.from_user.id
    user_info = await UserDAO.find_one_or_none(
        session=session_with_commit,
        filters=TelegramIDModel(telegram_id=user_id)
    )

    if user_info:
        return await message.answer(
            text=f'You are already in database',
            reply_markup=ikb_main()
        )

    values = UserModel(
        telegram_id=user_id,
        username=message.from_user.username
    )

    await UserDAO.add(session=session_with_commit, values=values)
    await message.answer(
        text=f'Congratulation! Now you can use Bear Budget!',
        reply_markup=ikb_main()
    )


@user_router.callback_query(F.data == 'income')
async def process_income(call: Message, state: FSMContext):
    await state.set_state(IncomeExpenseFSM.amount)
    await call.answer(
        text='Enter amount'
    )


@user_router.callback_query(F.data == 'settings')
async def process_settings(call: CallbackQuery):
    await call.message.edit_text(
        text='Settings',
        reply_markup=ikb_settings()
    )

@user_router.callback_query(F.data == 'settings_categories')
async def process_settings_categories(call: CallbackQuery, session_without_commit: AsyncSession):
    categories = await CategoryDAO.find_all(session=session_without_commit)

    await call.message.edit_text(
        text='Your categories',
        reply_markup=ikb_settings_categories(categories)
    )

@user_router.callback_query(F.data == 'add_new_category')
async def process_add_new_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(user_telegram_id=call.from_user.id)
    await state.set_state(AddCategoryFSM.type)
    await call.message.edit_text(
        text='Select type',
        reply_markup=ikb_income_expense()
    )
    await call.answer()

@user_router.callback_query(F.data == 'add_category_income', AddCategoryFSM.type)
async def process_add_income_category(call: CallbackQuery, state: FSMContext):
    await state.update_data(type='income')
    await state.set_state(AddCategoryFSM.name)
    await call.message.edit_text(text='Enter name')

@user_router.message(F.text, AddCategoryFSM.name)
async def process_name_category(message: Message, state: FSMContext, session_with_commit: AsyncSession):
    name = message.text
    await state.update_data(name=name)

    data = await state.get_data()
    await CategoryDAO.add(session=session_with_commit, values=CategoryModel(**data))
    await state.clear()
    await message.answer(text='Suck')

@user_router.message(F.text.isdigit(), IncomeExpenseFSM.amount)
async def process_enter_amount(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    bot_message = await message.answer(text='Successes')
    await asyncio.sleep(2)
    await bot_message.delete()


@user_router.message(~F.text.isdigit(), IncomeExpenseFSM.amount)
async def process_enter_amount(message: Message):
    bot_message = await message.answer(text='Enter a number')
    await asyncio.sleep(2)
    await bot_message.delete()
