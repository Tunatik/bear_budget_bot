import asyncio
from os import getenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from handlers import user_handlers
from models.models import Base, engine

load_dotenv()

TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

async def main():
    dp.include_router(user_handlers.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    asyncio.run(main())