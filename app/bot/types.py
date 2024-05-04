from typing import TypeAlias

from aiogram.types import CallbackQuery, Message

Event: TypeAlias = CallbackQuery | Message
