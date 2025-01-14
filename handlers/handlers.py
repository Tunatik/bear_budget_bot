from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao import UserDAO
from dao.models import User
from dao.shemas import TelegramIDModel, UserModel


user_router = Router()


@user_router.message(CommandStart())
async def process_cmd_start(message: Message, session_with_commit: AsyncSession):
    user_id = message.from_user.id
    user_info = await UserDAO.find_one_or_none(
        session=session_with_commit,
        filters=TelegramIDModel(telegram_id=user_id)
    )

    if user_info:
        return await message.answer(
            text=f'You are already in database'
        )

    values = UserModel(
        telegram_id=user_id,
        username=message.from_user.username
    )

    await UserDAO.add(session=session_with_commit, values=values)
    await message.answer(f'Congratulation! Now you can use Bear Budget!')