from database import execute, fetchall

async def add_set_post(channel_id: int, from_chat_id: int, message_id: int):
    await execute("""
    INSERT INTO set_posts (channel_id, from_chat_id, message_id)
    VALUES (?, ?, ?)
    """, (channel_id, from_chat_id, message_id))

async def get_set_posts(channel_id: int):
    return await fetchall(
        "SELECT * FROM set_posts WHERE channel_id=? ORDER BY id ASC",
        (channel_id,)
    )

async def clear_set_posts(channel_id: int):
    await execute("DELETE FROM set_posts WHERE channel_id=?", (channel_id,))
