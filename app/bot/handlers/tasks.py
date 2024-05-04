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
    text = m.ENTER_TASK_NAME_MSG.format(username=u.get_username(message))
    await message.answer(text)


@router.message(TaskInput.task_name)
async def task_name_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(task_name=message.text)
    await state.set_state(TaskInput.task_description)
    text = m.ENTER_TASK_DESCRIPTION_MSG.format(username=u.get_username(message))
    await message.answer(text)


@router.message(TaskInput.task_description)
async def task_description_handler(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(task_description=message.text)
    await state.clear()
    text = m.ADD_TASK_MSG.format(
        username=u.get_username(message),
        task=await tasks.create_task(**data),
    )
    await message.answer(text)


@router.message(filters.Command("tsk"))
async def list_tasks_handler(message: types.Message) -> None:
    """`/tsk` command handler. Creates the keyboard with the task names buttons."""
    text = m.TASK_LIST_MSG.format(username=u.get_username(message))
    reply_markup = u.get_markup(
        *[[(name, name)] for name in await tasks.get_all_tasks_names()]
    )
    await message.answer(text, reply_markup=reply_markup)


@router.message()
async def wrong_command_handler(message: types.Message) -> None:
    """Handles all messages except the commands `/start`, `/add`, `/tsk` and
    tips what to type."""
    text = m.WRONG_CMD_MSG.format(username=u.get_username(message))
    await message.answer(text)


@router.callback_query()
async def task_summary_handler(callback: types.CallbackQuery) -> None:
    """Handles all callback queries - finds a task by name and
    returns a summary of the chosen task."""
    text = m.TASK_SUMMARY_MSG.format(
        username=u.get_username(callback),
        name=callback.data,
        description=await tasks.get_task_description(task_name=callback.data),
    )
    await callback.message.edit_text(text)
