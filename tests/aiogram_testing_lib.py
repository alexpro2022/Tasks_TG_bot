import inspect
from datetime import datetime as dt
from types import MethodType
from typing import Any, Callable

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType
from aiogram.types import (
    CallbackQuery,
    Chat,
    DateTime,
    InlineKeyboardMarkup,
    Message,
    Update,
    User,
)

ID = 1


def info(item):
    from pprint import pprint

    pprint(item)
    assert 0


def get_chat(id: int = ID, type: str = "chat", **kwargs) -> Chat:
    return Chat(id=id, type=type, **kwargs)


def get_user(
    id: int = ID,
    is_bot: bool = False,
    first_name: str = "first_name",
    last_name: str = "last_name",
    username: str = "username",
    **kwargs,
) -> User:
    return User(
        id=id,
        is_bot=is_bot,
        first_name=first_name,
        last_name=last_name,
        username=username,
        **kwargs,
    )


def get_message(
    message_id: int = ID,
    date: DateTime = dt.now(),
    chat: Chat = get_chat(),
    from_user: User = get_user(),
    text: str = "Test message text",
    **kwargs,
) -> Message:
    return Message(
        message_id=message_id,
        date=date,
        chat=chat,
        from_user=from_user,
        text=text,
        **kwargs,
    )


def get_callback(
    id: str = f"{ID}",
    from_user: User = get_user(),
    chat_instance: str = "chat_instance",
    message: Message = get_message(),
    data: str | None = None,
    **kwargs,
) -> CallbackQuery:
    return CallbackQuery(
        id=id,
        from_user=from_user,
        chat_instance=chat_instance,
        message=message,
        data=data,
        **kwargs,
    )


def get_update(
    update_id: int = ID,
    event: Message | CallbackQuery | None = None,
    **kwargs,
) -> Update:
    if isinstance(event, Message):
        return Update(update_id=update_id, message=event, **kwargs)
    return Update(update_id=update_id, callback_query=event, **kwargs)


class StateMixin:
    fsm_context: FSMContext
    state: StateType = None
    check_state_empty: bool = False
    check_set_state: StateType = None
    check_state_data: Any | None = None

    async def get_state(self) -> str | None:
        return await self.fsm_context.get_state()

    async def state_empty(self) -> bool:
        return await self.get_state() is None

    async def setup_state(self, **kwargs) -> None:
        dispatcher: Dispatcher = kwargs.get("dispatcher")
        bot: Bot = kwargs.get("bot")
        self.fsm_context = dispatcher.fsm.get_context(
            bot=bot, chat_id=get_chat().id, user_id=get_user().id
        )
        await self.fsm_context.set_state(self.state)

    async def state_checks(self):
        if self.check_state_empty:
            assert await self.state_empty()
        if self.check_set_state is not None:
            self._assert(await self.get_state(), self.check_set_state)
        if self.check_state_data is not None:
            self._assert(await self.fsm_context.get_data(), self.check_state_data)
            await self.fsm_context.clear()


class BaseTestCase:
    """TODO: add description."""

    ASSERT_MSG: str = "\n\nACTUAL:\n{actual}\n\nEXPECTED:\n{expected}\n"
    update: Update | None = None
    handler: Callable | None = None
    handler_send_method: str | None = None  # aiogram method sending the message
    funcs_to_mock: tuple[tuple] | None = (
        None  # (module, method_name, mock_func=self.dummy_mock)
    )
    _mock_counter: int = 0
    # expected outputs
    expected_text: str | None = None
    expected_reply_markup: InlineKeyboardMarkup | None = None
    expected_mock_counter: int | None = None

    def _assert(self, actual, expected) -> None:
        assert actual == expected, self.ASSERT_MSG.format(
            actual=actual, expected=expected
        )

    def _find_handler_name_in_stack(self, level: int = 7) -> None:
        if self.handler is not None:
            handler_name = self.handler.__name__
            for i in range(level):
                if inspect.stack()[i][3] == handler_name:
                    return None
            assert 0, f"Cannot find the handler name `{handler_name}` in the stack."

    async def dummy_mock(self, *args, **kwargs) -> None:
        self._mock_counter += 1

    async def _message_mock(self, *args, **kwargs) -> Message:
        if args:
            self._assert(args[0], self.expected_text)
        if kwargs:
            self._assert(kwargs.get("text", self.expected_text), self.expected_text)
            self._assert(kwargs.get("reply_markup"), self.expected_reply_markup)
        self._find_handler_name_in_stack()
        self._mock_counter += 1
        return get_message()

    def _setup_funcs_to_mock(self, monkeypatch) -> None:
        """Mock functions(querying to db or external API, etc) inside handler"""
        if self.funcs_to_mock is not None:
            for t in self.funcs_to_mock:
                if len(t) == 3:
                    module, func_name, mock = t
                    mock = MethodType(  # provide accsess to self._mock_counter inside mock method
                        mock, self
                    )
                else:
                    module, func_name = t
                    mock = self.dummy_mock
                if isinstance(module, str):
                    from importlib import import_module

                    module = import_module(module)
                assert hasattr(
                    module, func_name
                ), f'Module {module} has no method "{func_name}"'
                monkeypatch.setattr(module, func_name, mock)

    async def _setup(self, monkeypatch, **kwargs) -> None:
        monkeypatch.setattr("aiogram.types.CallbackQuery.answer", self.dummy_mock)
        monkeypatch.setattr(self.handler_send_method, self._message_mock)
        self._setup_funcs_to_mock(monkeypatch)
        if hasattr(self, "setup_state"):
            await self.setup_state(**kwargs)

    async def test_router(
        self, monkeypatch, dispatcher: Dispatcher, bot: Bot, **kwargs
    ):
        await self._setup(monkeypatch, dispatcher=dispatcher, bot=bot, **kwargs)
        await dispatcher.feed_update(bot, self.update, **kwargs)
        if self.expected_mock_counter is not None:
            self._assert(self._mock_counter, self.expected_mock_counter)
        if hasattr(self, "state_checks"):
            await self.state_checks()


class MessageRouterTestCase(BaseTestCase):
    """
    Base testing class for message update routers.
    Mock the `handler_send_method` and check the parameters of it
    (Same idea as the `unittest.mock.AsyncMock.assert_called_once_with`).
    """

    message_text: str
    handler_send_method = "aiogram.types.Message.answer"
    expected_mock_counter = 1

    async def _setup(self, monkeypatch, **kwargs) -> None:
        if self.update is None:
            self.update = get_update(event=get_message(text=self.message_text))
        await super()._setup(monkeypatch, **kwargs)


class CallbackRouterTestCase(BaseTestCase):
    """
    Base testing class for callback_query update routers.
    Mock the `handler_send_method` and check the parameters of it
    (Same idea as the `unittest.mock.AsyncMock.assert_called_once_with`).
    """

    callback_data: str
    handler_send_method = "aiogram.types.Message.edit_text"
    expected_mock_counter = 2

    async def _setup(self, monkeypatch, **kwargs) -> None:
        if self.update is None:
            self.update = get_update(event=get_callback(data=self.callback_data))
        await super()._setup(monkeypatch, **kwargs)
