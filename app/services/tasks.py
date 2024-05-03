from dataclasses import dataclass


@dataclass
class Task:
    name: str
    description: str


async def save_task(task_name: str, task_description: str) -> Task:
    return Task(task_name, task_description)


async def get_all_names() -> list[str]:
    return ["TASK1", "TASK2", "TASK3"]
