import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bot.setup import create_bot, create_dispatcher
from app.config import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    bot = create_bot(settings.bot_token)
    dp = create_dispatcher()
    polling_task = asyncio.create_task(dp.start_polling(bot))
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
    logger.info("Telegram bot stopped")


app = FastAPI(title="AI Speaking Club", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
