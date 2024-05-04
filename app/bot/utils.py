from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.types import Event


def _get_dispatcher(*router_modules) -> Dispatcher:
    """Creates dispatcher and includes the routers.\n
    Params:
      `*router_modules` - modules containing local routers.
    """
    dp = Dispatcher()
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    for module in router_modules:
        dp.include_routers(module.__getattribute__("router"))
    return dp


def get_username(event: Event) -> str:
    """Returns user full name."""
    return event.from_user.full_name


def get_markup(*buttons: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру из переданных кнопок."""
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        bts = [
            InlineKeyboardButton(text=text, callback_data=callback_data)
            for text, callback_data in button
        ]
        kb_builder.row(*bts)
    return kb_builder.as_markup()
