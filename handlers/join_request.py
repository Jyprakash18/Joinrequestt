from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from models.users import upsert_user
from models.channels import upsert_channel
from services.latest_post import get_latest_post

router = Router()

@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest, bot: Bot):
    user = request.from_user
    user_chat_id = request.user_chat_id
    channel_id = request.chat.id

    await upsert_channel(
        channel_id=channel_id,
        title=request.chat.title,
        username=request.chat.username
    )

    await upsert_user(
        user_id=user.id,
        user_chat_id=user_chat_id,
        channel_id=channel_id,
        username=user.username,
        first_name=user.first_name
    )

    latest_post = await get_latest_post(channel_id)

    try:
        if latest_post:
            await bot.copy_message(
                chat_id=user_chat_id,
                from_chat_id=latest_post["from_chat_id"],
                message_id=latest_post["message_id"]
            )
        else:
            await bot.send_message(
                chat_id=user_chat_id,
                text="Post abhi set nahi hai. Admin se contact karein."
            )
    except (TelegramForbiddenError, TelegramBadRequest):
        # Agar 5 minute window expire ho gaya ya bot PM nahi kar paaya.
        pass
