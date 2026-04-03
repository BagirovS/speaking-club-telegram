from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="speaking_club")

WELCOME_TEXT = "Welcome to AI Speaking Club"


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT)
