from aiogram.fsm.state import State, StatesGroup

from app.bot.handlers.tasks import TaskInput


def test_task_input_class() -> None:
    assert issubclass(TaskInput, StatesGroup)
    assert isinstance(TaskInput.task_name, State)
    assert isinstance(TaskInput.task_description, State)
