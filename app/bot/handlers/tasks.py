from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services import tasks

from .. import messages as m
from .. import utils as u

router = Router(name=__name__)


class TaskInput(StatesGroup):
    task_name = State()
    task_description = State()


@router.message(filters.Command("add"))
async def add_task_handler(message: types.Message, state: FSMContext) -> None:
    """`/add` command handler. Starts dialog."""
    await state.set_state(TaskInput.task_name)
    text = m.ENTER_TASK_NAME.format(username=u.get_username(message))
    await message.answer(text)


@router.message(TaskInput.task_name)
async def task_name_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(task_name=message.text)
    await state.set_state(TaskInput.task_description)
    text = m.ENTER_TASK_DESCRIPTION.format(username=u.get_username(message))
    await message.answer(text)


@router.message(TaskInput.task_description)
async def task_description_handler(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(task_description=message.text)
    await state.clear()
    created_task = await tasks.save_task(**data)
    text = m.ADD_TASK_MSG.format(
        username=u.get_username(message),
        task=f"{created_task.name}\n{created_task.description}\n",
    )
    await message.answer(text)


@router.message(filters.Command("tsk"))
async def list_tasks_handler(message: types.Message) -> None:
    """`/tsk` command handler. Sends the message with the list of all tasks names."""
    text = m.TASK_LIST_MSG.format(
        username=u.get_username(message),
        tasks="\n".join(await tasks.get_all_names()),
    )
    await message.answer(text)
