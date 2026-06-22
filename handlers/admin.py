from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from config import config
from services.stats import build_stats_text
from services.broadcast import broadcast_text
from models.channels import list_channels

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in config.admins

@router.message(Command("stats"))
async def stats_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    await message.answer(await build_stats_text())

@router.message(Command("channels"))
async def channels_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    channels = await list_channels()

    if not channels:
        return await message.answer("No channels/groups saved yet.")

    text = "📢 Channels/Groups:\n\n"
    for ch in channels:
        text += f"• {ch['title'] or 'Unknown'} | `{ch['channel_id']}`\n"

    await message.answer(text, parse_mode="Markdown")

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    text = message.text.replace("/broadcast", "", 1).strip()

    if not text:
        return await message.answer("Usage:\n/broadcast Your message here")

    await message.answer("Broadcast started...")
    sent, failed = await broadcast_text(bot, text)

    await message.answer(
        f"✅ Broadcast complete.\n\nSent: {sent}\nFailed: {failed}"
    )
