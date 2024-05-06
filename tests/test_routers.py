from aiogram_testing_lib import (
    CallbackRouterTestCase,
    MessageRouterTestCase,
    StateMixin,
    get_user,
)

from app.bot import messages as m
from app.bot.handlers import start as s
from app.bot.handlers import tasks as t
from app.bot.utils import get_markup
from app.repositories.models import Task

TASK_NAME = "test_input_task_name"
TASK_DESCRIPTION = "test_input_task_description"
USERNAME_KWARGS = {"username": get_user().full_name}


class TestWrongCommandRouter(MessageRouterTestCase):
    message_text = "/wrong_command"
    handler = t.wrong_command_handler
    expected_text = m.WRONG_CMD_MSG.format(**USERNAME_KWARGS)


class TestStartCommandRouter(MessageRouterTestCase):
    message_text = "/start"
    handler = s.start_handler
    expected_text = m.GREETING_MSG.format(**USERNAME_KWARGS)


class TestAddCommandRouter(StateMixin, MessageRouterTestCase):
    message_text = "/add"
    handler = t.add_task_handler
    expected_text = m.ENTER_TASK_NAME_MSG.format(**USERNAME_KWARGS)
    check_set_state = t.TaskInput.task_name.state


class TestTaskNameRouter(StateMixin, MessageRouterTestCase):
    state = t.TaskInput.task_name.state
    handler = t.task_name_handler
    message_text = TASK_NAME
    expected_text = m.ENTER_TASK_DESCRIPTION_MSG.format(**USERNAME_KWARGS)
    check_set_state = t.TaskInput.task_description.state
    check_state_data = {"task_name": TASK_NAME}


class TestTaskDescriptionRouter(StateMixin, MessageRouterTestCase):
    async def mock_create_task(self, *args, **kwargs) -> str:
        self._mock_counter += 1
        created_task = Task(
            name=TASK_NAME,
            description=kwargs["task_description"],
        )
        return f"{created_task.name}\n{created_task.description}\n"

    state = t.TaskInput.task_description.state
    handler = t.task_description_handler
    message_text = TASK_DESCRIPTION
    expected_text = m.ADD_TASK_MSG.format(
        **USERNAME_KWARGS, task=f"{TASK_NAME}\n{TASK_DESCRIPTION}\n"
    )
    check_state_empty = True
    funcs_to_mock = (("services.tasks", "create_task", mock_create_task),)
    expected_mock_counter = 2


class TestListTaskRouter(MessageRouterTestCase):
    async def mock_crud_get_all(self, model):
        self._mock_counter += 1
        return [model(name=TASK_NAME, description=TASK_DESCRIPTION)]

    message_text = "/tsk"
    handler = t.list_tasks_handler
    expected_text = m.TASK_LIST_MSG.format(**USERNAME_KWARGS)
    expected_reply_markup = get_markup(
        [(TASK_NAME, TASK_NAME)],
    )
    funcs_to_mock = (("repositories.db.crud", "get_all", mock_crud_get_all),)
    expected_mock_counter = 2


class TestTaskSummaryRouter(CallbackRouterTestCase):
    async def mock_crud_get(self, model, **kwargs):
        self._mock_counter += 1
        return [model(description=TASK_DESCRIPTION, **kwargs)]

    callback_data = TASK_NAME
    handler = t.task_summary_handler
    expected_text = m.TASK_SUMMARY_MSG.format(
        **USERNAME_KWARGS,
        name=callback_data,
        description=TASK_DESCRIPTION,
    )
    funcs_to_mock = (("repositories.db.crud", "get", mock_crud_get),)
    expected_mock_counter = 3
