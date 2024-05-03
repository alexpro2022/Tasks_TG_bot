async def get_all_names() -> list[str]:
    return ["TASK1", "TASK2", "TASK3"]


async def save_task(task_name: str, task_description: str | None = None) -> None:
    # TODO: save task to DB
    pass
