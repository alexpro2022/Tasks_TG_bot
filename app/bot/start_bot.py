from aiogram import Bot, Dispatcher
from bot.config import conf
from bot.handlers import start
from bot.handlers.tasks import tasks_commands


async def start_bot() -> None:
    bot = Bot(token=conf.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(
        start.router,
        tasks_commands.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
