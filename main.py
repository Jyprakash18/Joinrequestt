import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from database import init_db

from handlers.start import router as start_router
from handlers.join_request import router as join_request_router
from handlers.channel_posts import router as channel_posts_router
from handlers.admin import router as admin_router

async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(join_request_router)
    dp.include_router(channel_posts_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
