from aiogram import Router, F
from aiogram.types import Message
from config import config
from models.channels import upsert_channel
from services.latest_post import add_set_post

router = Router()

@router.channel_post()
async def channel_post_handler(message: Message):
    # Sirf channel posts store honge.
    # Bot ko channel me admin hona chahiye.
    await upsert_channel(
        channel_id=message.chat.id,
        title=message.chat.title,
        username=message.chat.username
    )

    # Latest post save.
    await add_set_post(
        channel_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
