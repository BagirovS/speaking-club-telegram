"""Telegram bot (aiogram): routers, handlers, wiring."""

from app.bot.setup import create_bot, create_dispatcher

__all__ = ["create_bot", "create_dispatcher"]
