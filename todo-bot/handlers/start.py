from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-менеджер задач.\n\n"
        "Команды:\n"
        "/add — добавить задачу\n"
        "/list — список задач\n"
        "/done — отметить задачу выполненной\n"
        "/delete — удалить задачу\n"
        "/stats — статистика"
    )