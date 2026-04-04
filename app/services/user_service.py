from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.repositories.user_repository import UserRepository

LEVEL_CHOICES: frozenset[str] = frozenset({"A1", "A2", "B1", "B2", "C1", "C2"})


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)

    async def get_or_create_user(self, telegram_id: str) -> User:
        user = await self._users.get_by_telegram_id(telegram_id)
        if user is not None:
            return user
        try:
            user = await self._users.create(telegram_id)
            await self._session.commit()
            await self._session.refresh(user)
            return user
        except IntegrityError:
            await self._session.rollback()
            user = await self._users.get_by_telegram_id(telegram_id)
            if user is None:
                raise
            return user

    async def set_level(self, telegram_id: str, level: str) -> User:
        if level not in LEVEL_CHOICES:
            msg = f"Invalid level: {level!r}"
            raise ValueError(msg)
        user = await self._users.set_level(telegram_id, level)
        if user is None:
            msg = "User not found"
            raise LookupError(msg)
        await self._session.commit()
        await self._session.refresh(user)
        return user
