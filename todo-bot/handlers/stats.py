from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select, func
from database.models import Task

router = Router()

@router.message(Command("stats"))
async def cmd_stats(message: Message, session):
    result = await session.execute(
        select(
            func.count().label("total"),
            func.sum(Task.is_done.cast(int)).label("done")
        ).where(Task.user_id == message.from_user.id)
    )
    stats = result.one()
    total = stats.total or 0
    done = stats.done or 0
    await message.answer(
        f"📊 **Статистика:**\n"
        f"Всего задач: {total}\n"
        f"Выполнено: {done}\n"
        f"Осталось: {total - done}"
    )