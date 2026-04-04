from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService


@pytest.mark.asyncio
async def test_set_level_persists(async_session: AsyncSession) -> None:
    service = UserService(async_session)
    await service.get_or_create_user("42")

    await service.set_level("42", "C1")
    user = await service.get_or_create_user("42")
    assert user.level == "C1"


@pytest.mark.asyncio
async def test_set_level_invalid_raises(async_session: AsyncSession) -> None:
    service = UserService(async_session)
    await service.get_or_create_user("77")

    with pytest.raises(ValueError, match="Invalid level"):
        await service.set_level("77", "X9")


@pytest.mark.asyncio
async def test_set_level_unknown_user_raises(async_session: AsyncSession) -> None:
    service = UserService(async_session)

    with pytest.raises(LookupError, match="User not found"):
        await service.set_level("missing", "A1")
