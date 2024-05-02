from aiogram import Router, filters, types

router = Router(name=__name__)

GREETINGS = (
    "Привет, {username}! \n"
    "Для добавления задачи в БД - команда /add \n"
    "Для вывода списка задач - команда /tsk \n"
)


@router.message(filters.CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(GREETINGS.format(username=message.from_user.full_name))
