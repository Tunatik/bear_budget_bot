from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from models.db_utils import *
from keyboards.reply_kb import *

router = Router()

class FSMTransactionForm(StatesGroup):
    income = State()
    expenses = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Success') # TODO add welcome script
    await register_user(message)

async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if db_register_user(full_name=full_name, chat_id=chat_id):
        await message.answer('Registration completed', reply_markup=actions_kb())
    else:
        await message.answer('You are registered user')

@router.message(F.text == 'Income')
async def add_income(message: Message, state: FSMContext):
    await state.set_state(FSMTransactionForm.income)
    await message.answer(text='Enter Income')

@router.message(FSMTransactionForm.income)
async def process_income(message: Message, state: FSMContext):
    db_add_income(int(message.text))
    await state.clear()

@router.message(F.text == 'Expenses')
async def add_income(message: Message, state: FSMContext):
    await state.set_state(FSMTransactionForm.expenses)
    await message.answer(text='Enter Expenses')

@router.message(FSMTransactionForm.expenses)
async def process_expenses(message: Message, state: FSMContext):
    db_add_expenses(int(message.text))
    await state.clear()