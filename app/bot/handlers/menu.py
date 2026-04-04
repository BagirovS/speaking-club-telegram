import uuid

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.room_repository import RoomRepository
from app.services.user_service import LEVEL_CHOICES, UserService

router = Router(name="menu")

CB_FIND_ROOM = "menu:find_room"
CB_PROFILE = "menu:profile"
CB_LEVEL_PREFIX = "onboarding:level:"
CB_ROOM_PREFIX = "menu:room:"

WELCOME_TEXT = "Welcome to AI Speaking Club"
ONBOARDING_TEXT = "Choose your English level:"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Find a Room", callback_data=CB_FIND_ROOM))
    builder.row(InlineKeyboardButton(text="Profile", callback_data=CB_PROFILE))
    return builder.as_markup()


def level_selection_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code in sorted(LEVEL_CHOICES):
        builder.add(
            InlineKeyboardButton(text=code, callback_data=f"{CB_LEVEL_PREFIX}{code}"),
        )
    builder.adjust(3)
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession) -> None:
    service = UserService(session)
    user = await service.get_or_create_user(telegram_id=str(message.from_user.id))
    if user.level is None:
        await message.answer(ONBOARDING_TEXT, reply_markup=level_selection_keyboard())
    else:
        await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data.startswith(CB_LEVEL_PREFIX))
async def on_level_selected(callback: CallbackQuery, session: AsyncSession) -> None:
    if not callback.data or not callback.from_user:
        await callback.answer()
        return
    level = callback.data.removeprefix(CB_LEVEL_PREFIX)
    if level not in LEVEL_CHOICES:
        await callback.answer("Invalid level", show_alert=True)
        return
    service = UserService(session)
    try:
        await service.set_level(telegram_id=str(callback.from_user.id), level=level)
    except LookupError:
        await callback.answer("Please use /start first", show_alert=True)
        return
    await callback.answer()
    if callback.message:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == CB_FIND_ROOM)
async def on_find_room(callback: CallbackQuery, session: AsyncSession) -> None:
    await callback.answer()
    if not callback.message:
        return
    repo = RoomRepository(session)
    rooms = await repo.list_all()
    if not rooms:
        await callback.message.answer("No rooms available yet.")
        return
    builder = InlineKeyboardBuilder()
    for room in rooms:
        builder.row(
            InlineKeyboardButton(
                text=room.name,
                callback_data=f"{CB_ROOM_PREFIX}{room.id}",
            ),
        )
    await callback.message.answer("Choose a room:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith(CB_ROOM_PREFIX))
async def on_room_selected(callback: CallbackQuery, session: AsyncSession) -> None:
    if not callback.data:
        await callback.answer()
        return
    raw_id = callback.data.removeprefix(CB_ROOM_PREFIX)
    try:
        room_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Invalid room", show_alert=True)
        return
    repo = RoomRepository(session)
    room = await repo.get_by_id(room_id)
    if room is None:
        await callback.answer("Room not found", show_alert=True)
        return
    await callback.answer()
    if callback.message:
        await callback.message.answer(f"Joining room: {room.name}")


@router.callback_query(F.data == CB_PROFILE)
async def on_profile(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.answer("Profile coming soon")
