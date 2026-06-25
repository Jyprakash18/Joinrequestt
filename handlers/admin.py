from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from config import config
from services.stats import build_stats_text
from services.broadcast import broadcast_text
from models.channels import list_channels
from services.latest_post import add_set_post, clear_set_posts

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
    from services.latest_post import save_latest_post

@router.message(Command("setpost"))
async def setpost_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    if not message.reply_to_message:
        return await message.answer(
            "Usage:\n"
            "1. Channel ka post bot me forward karo\n"
            "2. Us forwarded post par reply karke:\n"
            "/setpost CHANNEL_ID"
        )

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Channel ID do:\n/setpost -1001234567890")

    channel_id = int(parts[1])

    await save_latest_post(
        channel_id=channel_id,
        from_chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id
    )

    await message.answer("✅ Is channel ke liye post set ho gaya.")
@router.message(Command("setpost"))
async def setpost_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    if not message.reply_to_message:
        return await message.answer(
            "Post par reply karke command do:\n"
            "/setpost -100xxxxxxxxxx"
        )

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Channel ID missing.")

    channel_id = int(parts[1])

    await save_latest_post(
        channel_id=channel_id,
        from_chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id
    )

    await message.answer("✅ Post set ho gaya.")

@router.message(Command("addpost"))
async def addpost_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    if not message.reply_to_message:
        return await message.answer("Post par reply karke:\n/addpost -100xxxxxxxxxx")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Channel ID missing.")

    channel_id = int(parts[1])

    await add_set_post(
        channel_id=channel_id,
        from_chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id
    )

    await message.answer("✅ Post add ho gaya.")

@router.message(Command("clearposts"))
async def clearposts_handler(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Admin only.")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Use:\n/clearposts -100xxxxxxxxxx")

    channel_id = int(parts[1])
    await clear_set_posts(channel_id)

    await message.answer("🗑 Saare posts clear ho gaye.")
