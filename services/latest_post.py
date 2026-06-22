from database import execute, fetchone

async def save_latest_post(channel_id: int, from_chat_id: int, message_id: int):
    await execute("""
    INSERT INTO latest_posts (channel_id, from_chat_id, message_id)
    VALUES (?, ?, ?)
    ON CONFLICT(channel_id) DO UPDATE SET
        from_chat_id=excluded.from_chat_id,
        message_id=excluded.message_id,
        updated_at=CURRENT_TIMESTAMP
    """, (channel_id, from_chat_id, message_id))

async def get_latest_post(channel_id: int):
    return await fetchone(
        "SELECT from_chat_id, message_id FROM latest_posts WHERE channel_id=?",
        (channel_id,)
    )
