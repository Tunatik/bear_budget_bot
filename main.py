import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger

from config import bot, dp
from middleware.database_connection import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from handlers.handlers import user_router


async def set_commands():
    commands = [
        BotCommand(command='start', description='start'),
        BotCommand(command='help', description='help'),
    ]

    await bot.set_my_commands(commands)


async def start_bot():
    await set_commands()
    logger.info('bot launched successfully')


async def stop_bot():
    logger.info('bot stopped')


async def main():
    dp.update.middleware(DatabaseMiddlewareWithCommit())
    dp.update.middleware(DatabaseMiddlewareWithoutCommit())

    dp.include_router(user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())