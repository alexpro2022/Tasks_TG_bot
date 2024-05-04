from . import emoji

BOT_SPEAKING = f"{emoji.BABY_ANGEL}\n\n"
USERNAME = "{username},\n"
HEADER = BOT_SPEAKING + USERNAME

GREETING_MSG = (
    BOT_SPEAKING + "Привет, {username}! \n"
    "Я маленький бот, умею выполнять всего две команды:\n"
    "   - для добавления задачи в БД - команда /add \n"
    "   - для вывода списка задач - команда /tsk "
)
ENTER_TASK_NAME_MSG = HEADER + "Напиши название задачи" + emoji.WRITING_HAND
ENTER_TASK_DESCRIPTION_MSG = HEADER + "Напиши описание задачи" + emoji.WRITING_HAND
ADD_TASK_MSG = HEADER + "Задача \n{task} сохранена в БД." + emoji.SAVE
TASK_LIST_MSG = HEADER + "Список задач: \n" + emoji.LIST
TASK_SUMMARY_MSG = HEADER + "\nЗадача:\n  {name}\n\nОписание:\n  {description}"
WRONG_CMD_MSG = HEADER + "пока я понимаю только команды /add и /tsk" + emoji.STOP
