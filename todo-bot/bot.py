import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import create_db
from middlewares.db_session import DbSessionMiddleware
from handlers import start, add_task, list_tasks, done, delete, stats

logging.basicConfig(level=logging.INFO)


async def main():
    await create_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    # Middleware
    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())
    # Роутеры
    dp.include_router(start.router)
    dp.include_router(add_task.router)
    dp.include_router(list_tasks.router)
    dp.include_router(done.router)
    dp.include_router(delete.router)
    dp.include_router(stats.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())