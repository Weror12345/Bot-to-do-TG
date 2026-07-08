from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from database.models import Task

router = Router()

@router.callback_query(F.data.startswith("done_"))
async def mark_done(callback: CallbackQuery, session):
    task_id = int(callback.data.split("_")[1])
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        await callback.answer("Задача не найдена.")
        return
    task.is_done = True
    await session.commit()
    await callback.answer("Задача отмечена выполненной!")
    await callback.message.edit_text(f"✅ {task.title} — выполнено!")