from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.task_states import AddTask
from database.models import Task

router = Router()

@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddTask.title)
    await message.answer("Введите название задачи:")

@router.message(AddTask.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTask.description)
    await message.answer("Введите описание задачи (или напишите 'пропустить'):")

@router.message(AddTask.description)
async def process_description(message: Message, state: FSMContext):
    if message.text.lower() == "пропустить":
        await state.update_data(description=None)
    else:
        await state.update_data(description=message.text)
    await state.set_state(AddTask.deadline)
    await message.answer("Введите дедлайн в формате ГГГГ-ММ-ДД ЧЧ:ММ (или 'пропустить'):")

@router.message(AddTask.deadline)
async def process_deadline(message: Message, state: FSMContext, session):
    if message.text.lower() == "пропустить":
        deadline = None
    else:
        try:
            deadline = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        except ValueError:
            await message.answer("Неверный формат. Попробуйте ещё раз или 'пропустить'.")
            return
    data = await state.get_data()
    task = Task(
        user_id=message.from_user.id,
        title=data["title"],
        description=data.get("description"),
        deadline=deadline
    )
    session.add(task)
    await session.commit()
    await state.clear()
    await message.answer(f"✅ Задача «{task.title}» добавлена!")

@router.message(AddTask.title)
async def invalid_title(message: Message):
    await message.answer("Пожалуйста, введите корректное название.")