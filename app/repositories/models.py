from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .db.base import Base

TASK_NAME_MAX_LENGTH = 50
TASK_DESCRIPTION_MAX_LENGTH = 500


class Task(Base):
    name: Mapped[str] = mapped_column(String(TASK_NAME_MAX_LENGTH), unique=True)
    description: Mapped[str] = mapped_column(
        String(TASK_DESCRIPTION_MAX_LENGTH), default="No description"
    )

    def __repr__(self) -> str:
        return (
            f"{super().__repr__()}\nname: {self.name}\ndescription: {self.description}"
        )
