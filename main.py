 import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import config
from database import init_db

# Aapke existing routers import ho rahe hain
from handlers.start import router as start_router
from handlers.join_request import router as join_request_router
from handlers.channel_posts import router as channel_posts_router
from handlers.admin import router as admin_router

# --- Dummy Web Server Functions ---
async def handle_dummy_request(request):
    return web.Response(text="Bot is running on Render!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_dummy_request)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render PORT environment variable deta hai, default 8080 rakh rahe hain
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Dummy web server started on port {port}")
# -----------------------------------

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
    
    # Render ke liye dummy server start kar rahe hain polling se pehle
    await start_dummy_server()
    
    # Ab bot polling start hogi
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
)
