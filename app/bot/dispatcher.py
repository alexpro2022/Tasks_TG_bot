from aiogram import Dispatcher

from . import utils as u
from .handlers import start, tasks


def get_dispatcher() -> Dispatcher:
    """Returns bot dispatcher."""
    return u._get_dispatcher(start, tasks)
