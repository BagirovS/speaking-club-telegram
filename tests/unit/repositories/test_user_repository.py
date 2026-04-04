from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_and_get_by_telegram_id(async_session: AsyncSession) -> None:
    repo = UserRepository(async_session)
    created = await repo.create("12345")
    await async_session.commit()

    found = await repo.get_by_telegram_id("12345")
    assert found is not None
    assert found.id == created.id
    assert found.telegram_id == "12345"
    assert found.level is None


@pytest.mark.asyncio
async def test_set_level(async_session: AsyncSession) -> None:
    repo = UserRepository(async_session)
    await repo.create("999")
    await async_session.commit()

    updated = await repo.set_level("999", "B1")
    assert updated is not None
    assert updated.level == "B1"
    await async_session.commit()

    again = await repo.get_by_telegram_id("999")
    assert again is not None
    assert again.level == "B1"


@pytest.mark.asyncio
async def test_set_level_missing_user(async_session: AsyncSession) -> None:
    repo = UserRepository(async_session)
    assert await repo.set_level("nope", "A1") is None
