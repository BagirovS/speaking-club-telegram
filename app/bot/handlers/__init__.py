from aiogram import Router

from app.bot.handlers.menu import router as menu_router

router = Router(name="speaking_club")
router.include_router(menu_router)
