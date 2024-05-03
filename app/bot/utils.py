from aiogram import Dispatcher, types


def _get_dispatcher(*router_modules) -> Dispatcher:
    """Creates dispatcher and includes the routers.\n
    Params:
      `*router_modules` - modules containing local routers.
    """
    dp = Dispatcher()
    for module in router_modules:
        dp.include_routers(module.__getattribute__("router"))
    return dp


def get_username(message: types.Message) -> str:
    """Returns user full name."""
    return message.from_user.full_name


'''
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.utils.keyboard import InlineKeyboardMarkup


async def bot_answer(  # type: ignore[return]
    event: TelegramObject,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str = ParseMode.HTML,
) -> Message | None:
    """Отправляет сообщение в чат."""
    kwargs = {'parse_mode': parse_mode, 'reply_markup': reply_markup}
    if isinstance(event, Message):
        return await event.answer(text, **kwargs)
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, **kwargs)
        await event.answer()
'''
