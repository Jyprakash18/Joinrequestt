# Telegram Join Request AutoPost Bot

Aiogram 3.x based Telegram bot.

## Features

- Chat join request detect
- `user_chat_id` capture
- Instant private message
- Latest channel post auto copy
- Multiple channel/group support
- SQLite database
- `/stats`
- `/broadcast`
- `/channels`

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
ADMINS=YOUR_TELEGRAM_USER_ID
DATABASE_PATH=data/bot.db
```

Run:

```bash
python main.py
```

## Telegram Setup

1. Bot ko channel/group me admin banao.
2. Invite users via link / approve join requests permission do.
3. Channel/group me join request enabled invite link banao.
4. Channel me ek post karo, bot latest post save karega.
5. User jab Request to Join karega, bot usko latest post PM karega.

## Note

Telegram `user_chat_id` temporary hota hai. Bot join request ke baad limited time window me private message bhej sakta hai.
