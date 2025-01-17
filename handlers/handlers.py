import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from utils.utils import delete_bot_message_with_delay
from config import bot
from dao.dao import UserDAO, CategoryDAO
from dao.models import User
from dao.shemas import TelegramIDModel, UserModel, CategoryModel
from keyboards.reply import *
from keyboards.inline import *


user_router = Router()

class IncomeExpenseFSM(StatesGroup):
    amount = State()


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


@user_router.callback_query(F.data == 'main')
async def process_main(call: CallbackQuery):
    await call.message.edit_text(
        text='Main menu',
        reply_markup=ikb_main()
    )


@user_router.callback_query(F.data == 'income')
async def process_income(call: Message, state: FSMContext):
    await state.set_state(IncomeExpenseFSM.amount)
    await call.answer(
        text='Enter amount'
    )

@user_router.message(F.text.isdigit(), IncomeExpenseFSM.amount)
async def process_enter_amount(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    bot_message = await message.answer(text='Successes')
    await delete_bot_message_with_delay(bot_message)


@user_router.message(~F.text.isdigit(), IncomeExpenseFSM.amount)
async def process_enter_amount(message: Message):
    bot_message = await message.answer(text='Enter a number')
    await delete_bot_message_with_delay(bot_message)

