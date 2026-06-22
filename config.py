import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    bot_token: str
    admins: set[int]
    database_path: str

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN missing. Create .env file from .env.example")

    admins_raw = os.getenv("ADMINS", "")
    admins = {
        int(x.strip())
        for x in admins_raw.split(",")
        if x.strip().isdigit()
    }

    return Config(
        bot_token=token,
        admins=admins,
        database_path=os.getenv("DATABASE_PATH", "data/bot.db")
    )

config = load_config()
