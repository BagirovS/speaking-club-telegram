from __future__ import annotations

import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Room
from app.repositories.room_repository import RoomRepository


@pytest.mark.asyncio
async def test_list_all_orders_by_name(async_session: AsyncSession) -> None:
    repo = RoomRepository(async_session)
    async_session.add_all(
        [
            Room(name="Zebra", topic="z", invite_link="https://t.me/+z"),
            Room(name="Alpha", topic="a", invite_link="https://t.me/+a"),
        ],
    )
    await async_session.commit()

    rooms = await repo.list_all()
    assert [r.name for r in rooms] == ["Alpha", "Zebra"]


@pytest.mark.asyncio
async def test_get_by_id_found(async_session: AsyncSession) -> None:
    repo = RoomRepository(async_session)
    rid = uuid.uuid4()
    async_session.add(Room(id=rid, name="Travel", topic="t", invite_link="https://t.me/+x"))
    await async_session.commit()

    found = await repo.get_by_id(rid)
    assert found is not None
    assert found.name == "Travel"
    assert found.invite_link == "https://t.me/+x"


@pytest.mark.asyncio
async def test_get_by_id_missing(async_session: AsyncSession) -> None:
    repo = RoomRepository(async_session)
    assert await repo.get_by_id(uuid.uuid4()) is None
