import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from dao.shemas import TelegramIDModel
from dao.dao import CategoryDAO



async def delete_bot_message_with_delay(bot_message: Message, delay: int = 2):
    await asyncio.sleep(delay)
    await bot_message.delete()


async def get_categories_from_telegram_id(telegram_id: int, session: AsyncSession):
    categories = await CategoryDAO.find_all(session=session,
                                            filters=TelegramIDModel(telegram_id=telegram_id))
    return categories