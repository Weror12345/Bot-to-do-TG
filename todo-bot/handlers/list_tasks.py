from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from database.models import Task
from keyboards.inline import get_tasks_keyboard, get_task_actions_keyboard

router = Router()

@router.message(Command("list"))
async def cmd_list(message: Message, session):
    await show_tasks(message, session, user_id=message.from_user.id, page=0)

@router.callback_query(F.data.startswith("page_"))
async def paginate(callback: CallbackQuery, session):
    page = int(callback.data.split("_")[1])
    await show_tasks(callback.message, session, user_id=callback.from_user.id, page=page, edit=True)
    await callback.answer()

async def show_tasks(message, session, user_id: int, page: int = 0, edit: bool = False):
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    if not tasks:
        if edit:
            await message.edit_text("У вас пока нет задач.")
        else:
            await message.answer("У вас пока нет задач.")
        return
    text = "📋 **Ваши задачи:**\n" + "\n".join(
        f"{'✅' if t.is_done else '⬜'} {t.title}" for t in tasks
    )
    kb = get_tasks_keyboard(tasks, page)
    if edit:
        await message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data.startswith("task_"))
async def task_detail(callback: CallbackQuery, session):
    task_id = int(callback.data.split("_")[1])
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        await callback.answer("Задача не найдена.")
        return
    deadline = task.deadline.strftime("%d.%m.%Y %H:%M") if task.deadline else "нет"
    text = (
        f"📌 **{task.title}**\n"
        f"Описание: {task.description or 'нет'}\n"
        f"Дедлайн: {deadline}\n"
        f"Статус: {'✅ выполнена' if task.is_done else '⬜ в процессе'}"
    )
    await callback.message.edit_text(text, reply_markup=get_task_actions_keyboard(task.id), parse_mode="Markdown")
    await callback.answer()