from aiogram import Bot, Dispatcher


def test_bot_fixture(bot: Bot) -> None:
    assert isinstance(bot, Bot)


def test_dispatcher_fixture(dispatcher: Dispatcher) -> None:
    assert isinstance(dispatcher, Dispatcher)
