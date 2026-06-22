from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "✅ Bot active hai.\n\n"
        "Request to Join karne ke baad yahi bot aapko latest post bhejega."
    )
