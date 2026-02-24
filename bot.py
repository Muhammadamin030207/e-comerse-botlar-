import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from handlers.start import router as start_router
from handlers.register import router as register_router
from databases.database import Database
from handlers.profile import router as profile_router
from handlers.products.product import router as products_router

from handlers.admin.admin import router as admin_router


async def main():
    bot = Bot(token=config.BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())

    db = Database()
    await db.connect()

    dp["db"] = db

    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)
    dp.include_router(products_router)
    
    dp.include_router(admin_router)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
