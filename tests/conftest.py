import pytest
from aiogram import Bot, Dispatcher

from app.bot.dispatcher import get_dispatcher


@pytest.fixture(scope="session")
def bot() -> Bot:
    return Bot(token="1111111111:AAAAAAAAAAAAAAAAA-BBB_CCCCCCCCCCCCC")


@pytest.fixture(scope="session")
def dispatcher() -> Dispatcher:
    return get_dispatcher()
