from aiogram.fsm.state import State, StatesGroup

class AddTask(StatesGroup):
    title = State()
    description = State()
    deadline = State()