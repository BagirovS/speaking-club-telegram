from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService

router = Router(name="menu")

CB_FIND_ROOM = "menu:find_room"
CB_PROFILE = "menu:profile"

WELCOME_TEXT = "Welcome to AI Speaking Club"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Find a Room", callback_data=CB_FIND_ROOM))
    builder.row(InlineKeyboardButton(text="Profile", callback_data=CB_PROFILE))
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession) -> None:
    service = UserService(session)
    await service.get_or_create_user(telegram_id=str(message.from_user.id))
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == CB_FIND_ROOM)
async def on_find_room(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.answer("Loading rooms...")


@router.callback_query(F.data == CB_PROFILE)
async def on_profile(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.answer("Profile coming soon")
