from database import execute, fetchall

async def upsert_channel(channel_id: int, title: str | None, username: str | None):
    await execute("""
    INSERT INTO channels (channel_id, title, username)
    VALUES (?, ?, ?)
    ON CONFLICT(channel_id) DO UPDATE SET
        title=excluded.title,
        username=excluded.username
    """, (channel_id, title, username))

async def list_channels():
    return await fetchall("SELECT * FROM channels ORDER BY created_at DESC")
