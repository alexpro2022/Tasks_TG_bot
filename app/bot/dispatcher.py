from aiogram import Dispatcher
from bot.handlers import start, tasks


def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_routers(
        start.router,
        tasks.router,
    )
    return dp
