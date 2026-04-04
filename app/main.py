import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bot.setup import create_bot, create_dispatcher
from app.config import get_settings
from app.db.session import create_engine, create_session_factory

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings.database_url)
    session_factory = create_session_factory(engine)
    bot = create_bot(settings.bot_token)
    dp = create_dispatcher(session_factory)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.bot = bot
    app.state.dispatcher = dp
    app.state.polling_task = polling_task
    logger.info("Telegram bot polling started")
    yield
    await dp.stop_polling()
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()
    await engine.dispose()
    logger.info("Telegram bot stopped")


app = FastAPI(title="AI Speaking Club", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
