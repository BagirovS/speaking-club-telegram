from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.bot.handlers import router
from app.bot.middleware import DbSessionMiddleware


def create_bot(token: str) -> Bot:
    return Bot(token=token, default=DefaultBotProperties())


def create_dispatcher(session_factory: async_sessionmaker[AsyncSession]) -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_factory))
    dp.include_router(router)
    return dp
