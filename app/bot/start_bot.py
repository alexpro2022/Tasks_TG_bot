from aiogram import Bot
from bot.config import conf
from bot.dispatcher import get_dispatcher


async def start_bot() -> None:
    bot = Bot(token=conf.bot_token.get_secret_value())
    dp = get_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
