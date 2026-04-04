from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Room


class RoomRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Room]:
        result = await self._session.execute(select(Room).order_by(Room.name.asc()))
        return list(result.scalars().all())

    async def get_by_id(self, room_id: uuid.UUID) -> Room | None:
        result = await self._session.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none()
