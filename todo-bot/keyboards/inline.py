from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_tasks_keyboard(tasks: list, page: int = 0, per_page: int = 5):
    builder = InlineKeyboardBuilder()
    start = page * per_page
    end = start + per_page
    for task in tasks[start:end]:
        done_emoji = "✅" if task.is_done else "⬜"
        builder.button(
            text=f"{done_emoji} {task.title[:30]}",
            callback_data=f"task_{task.id}"
        )
    builder.adjust(1)
    # пагинация
    if page > 0:
        builder.button(text="◀️ Назад", callback_data=f"page_{page-1}")
    if end < len(tasks):
        builder.button(text="Вперёд ▶️", callback_data=f"page_{page+1}")
    return builder.as_markup()

def get_task_actions_keyboard(task_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✔️ Выполнено", callback_data=f"done_{task_id}")
    builder.button(text="❌ Удалить", callback_data=f"del_{task_id}")
    builder.adjust(2)
    return builder.as_markup()