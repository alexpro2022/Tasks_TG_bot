from aiogram import Router, filters, types
from constants import GREETING_MSG

from .. import utils as u

router = Router(name=__name__)


@router.message(filters.CommandStart())
async def start_handler(message: types.Message) -> None:
    """`/start` command handler."""
    text = GREETING_MSG.format(username=u.get_username(message))
    await message.answer(text)
