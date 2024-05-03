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
