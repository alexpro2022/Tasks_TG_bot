from aiogram import Router, filters, types

router = Router(name=__name__)


@router.message(filters.Command("add"))
async def add(message: types.Message) -> None:
    await message.answer("add")


@router.message(filters.Command("tsk"))
async def tasks(message: types.Message) -> None:
    await message.answer("tsk")
