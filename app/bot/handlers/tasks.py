from aiogram import Router, filters, types
from constants import ADD_TASK_MSG, TASK_LIST_MSG
from services import tasks

from .. import utils as u

router = Router(name=__name__)


@router.message(filters.Command("add"))
async def add_task_handler(message: types.Message) -> None:
    """`/add` command handler. Starts dialog and saves the input to DB."""
    # TODO: start fms, get task name and description, close fms
    task_name = "TASK"
    task_descr = "TASK DESCRIPTION"
    await tasks.save_task(task_name, task_descr)
    text = ADD_TASK_MSG.format(
        username=u.get_username(message),
        task=f"{task_name}\n{task_descr}\n",
    )
    await message.answer(text)


@router.message(filters.Command("tsk"))
async def list_tasks_handler(message: types.Message) -> None:
    """`/tsk` command handler. Sends the message with the list of all tasks names."""
    text = TASK_LIST_MSG.format(
        username=u.get_username(message),
        tasks="\n".join(await tasks.get_all_names()),
    )
    await message.answer(text)
