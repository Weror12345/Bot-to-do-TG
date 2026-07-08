from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from database.models import Task

router = Router()

@router.callback_query(F.data.startswith("del_"))
async def delete_task(callback: CallbackQuery, session):
    task_id = int(callback.data.split("_")[1])
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        await callback.answer("Задача не найдена.")
        return
    title = task.title
    await session.delete(task)
    await session.commit()
    await callback.answer(f"Задача «{title}» удалена!")
    await callback.message.edit_text(f"🗑 Задача «{title}» удалена.")