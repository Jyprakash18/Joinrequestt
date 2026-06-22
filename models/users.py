from database import execute, fetchall, fetchone

async def upsert_user(user_id: int, user_chat_id: int, channel_id: int, username: str | None, first_name: str | None):
    await execute("""
    INSERT INTO users (user_id, user_chat_id, username, first_name, channel_id, requests_count)
    VALUES (?, ?, ?, ?, ?, 1)
    ON CONFLICT(user_id) DO UPDATE SET
        user_chat_id=excluded.user_chat_id,
        username=excluded.username,
        first_name=excluded.first_name,
        channel_id=excluded.channel_id,
        requests_count=requests_count + 1,
        is_active=1,
        updated_at=CURRENT_TIMESTAMP
    """, (user_id, user_chat_id, username, first_name, channel_id))

async def get_all_active_users():
    return await fetchall("SELECT user_id, user_chat_id FROM users WHERE is_active=1")

async def mark_inactive(user_id: int):
    await execute("UPDATE users SET is_active=0 WHERE user_id=?", (user_id,))

async def count_users():
    row = await fetchone("""
    SELECT
        COUNT(*) AS total_users,
        SUM(is_active) AS active_users,
        SUM(requests_count) AS total_requests
    FROM users
    """)
    return row
