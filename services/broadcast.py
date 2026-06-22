import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from models.users import get_all_active_users, mark_inactive

async def broadcast_text(bot: Bot, text: str):
    users = await get_all_active_users()

    sent = 0
    failed = 0

    for user in users:
        try:
            await bot.send_message(chat_id=user["user_chat_id"], text=text)
            sent += 1
            await asyncio.sleep(0.05)
        except TelegramForbiddenError:
            await mark_inactive(user["user_id"])
            failed += 1
        except TelegramBadRequest:
            failed += 1

    return sent, failed
