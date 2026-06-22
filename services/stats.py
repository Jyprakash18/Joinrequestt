from models.users import count_users
from models.channels import list_channels

async def build_stats_text():
    users = await count_users()
    channels = await list_channels()

    total_users = users["total_users"] or 0
    active_users = users["active_users"] or 0
    total_requests = users["total_requests"] or 0

    return (
        "📊 Bot Statistics\n\n"
        f"Total Users: {total_users}\n"
        f"Active Users: {active_users}\n"
        f"Total Join Requests: {total_requests}\n"
        f"Connected Channels/Groups: {len(channels)}"
    )
