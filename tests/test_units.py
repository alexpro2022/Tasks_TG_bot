import pytest
from aiogram.fsm.state import State, StatesGroup

from app.bot.handlers.tasks import TaskInput
from app.repositories.models import Task


def test_task_input_class() -> None:
    assert issubclass(TaskInput, StatesGroup)
    assert isinstance(TaskInput.task_name, State)
    assert isinstance(TaskInput.task_description, State)


task_model_fields = pytest.mark.parametrize("field_name", ("id", "name", "description"))


@task_model_fields
def test_task_model_attr(field_name: str) -> None:
    assert hasattr(Task, field_name)


@task_model_fields
def test_task_model_repr(field_name: str) -> None:
    representation = repr(Task())
    assert representation.find(field_name) != -1


def test_asdict() -> None:
    data = {"name": "test_as_dict_name", "description": "test_as_dict_description"}
    obj = Task(**data)._asdict()
    assert isinstance(obj, dict)
    for key in data:
        assert obj[key] == data[key]
