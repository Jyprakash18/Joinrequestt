from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from models.users import upsert_user
from models.channels import upsert_channel
from services.latest_post import get_set_posts

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

    posts = await get_set_posts(channel_id)

    # Yeh hissa ab function ke andar hai (indented properly)
    try:
        if posts:
            for post in posts:
                await bot.copy_message(
                    chat_id=user_chat_id,
                    from_chat_id=post["from_chat_id"],
                    message_id=post["message_id"]
                )
        else:
            await bot.send_message(
                chat_id=user_chat_id,
                text="Post abhi set nahi hai."
            )
    except (TelegramForbiddenError, TelegramBadRequest):
        # Agar user bot ko block kar de ya window expire ho jaye, toh bot crash nahi hoga
        pass
