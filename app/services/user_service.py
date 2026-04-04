from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepository(session)

    async def get_or_create_user(self, telegram_id: str) -> User:
        user = await self._users.get_by_telegram_id(telegram_id)
        if user is not None:
            return user
        user = await self._users.create(telegram_id)
        await self._session.commit()
        await self._session.refresh(user)
        return user
