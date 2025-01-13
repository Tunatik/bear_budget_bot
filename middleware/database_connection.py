from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from dao.model_base import engine, async_session_maker, AsyncSession


class BaseDatabaseMiddleware(BaseMiddleware):
    """Base middleware class for connection with database"""
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            self.set_session(data, session)
            try:
                result = await handler(event, data)
                await self.after_handler(session)
                return result
            except Exception as e:
                await session.rollback()
                raise e

    def set_session(self, data: Dict[str, Any], session: AsyncSession):
        raise NotImplementedError("This method must be realise in subclasses")

    async def after_handler(self, session: AsyncSession):
        pass


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session: AsyncSession):
        data['session_without_commit'] = session


class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session: AsyncSession):
        data['session_with_commit'] = session

    async def after_handler(self, session: AsyncSession):
        await session.commit()