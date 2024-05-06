from uuid import uuid4

import pytest
from aiogram.fsm.state import State, StatesGroup

from app.bot.handlers.tasks import TaskInput
from app.repositories.models import Task
from app.services.tasks import create_task

TASK_NAME = "test_task_name"
TASK_DESCRIPTION = "test_task_description"
EXCEPTION_MSG = "TEST"


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


def test_task_model_asdict() -> None:
    data = {
        "id": uuid4(),
        "name": "test_as_dict_name",
        "description": "test_as_dict_description",
    }
    obj = Task(**data)
    assert isinstance(obj, Task)
    assert isinstance(obj._asdict(), dict)
    assert obj._asdict() == data


async def test_create_task_return_task_info(monkeypatch) -> None:
    async def mock_crud_create(task):
        return task

    monkeypatch.setattr("repositories.db.crud.create", mock_crud_create)
    result = await create_task(TASK_NAME, TASK_DESCRIPTION)
    assert result == f"{TASK_NAME}\n{TASK_DESCRIPTION}\n"


async def test_create_task_return_exc_info(monkeypatch) -> None:
    async def mock_crud_create(task):
        from repositories.exceptions import ObjectExistsError

        raise ObjectExistsError(EXCEPTION_MSG)

    monkeypatch.setattr("repositories.db.crud.create", mock_crud_create)
    result = await create_task(TASK_NAME, TASK_DESCRIPTION)
    assert result == f"{EXCEPTION_MSG}\n"
