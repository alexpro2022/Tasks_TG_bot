from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..exceptions import ObjectExistsError, ObjectNotFoundError
from .dependencies import async_session


async def create(obj, asession: async_sessionmaker[AsyncSession] = async_session):
    async with asession() as session:
        session.add(obj)
        try:
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            raise ObjectExistsError("Объект уже существует.")
        await session.refresh(obj)
    return obj


async def get(
    model,
    asession: async_sessionmaker[AsyncSession] = async_session,
    exception: bool = False,
    **kwargs,
):
    stmt = select(model).filter_by(**kwargs)
    async with asession() as session:
        result = await session.scalars(stmt)
    res = result.all() if kwargs.get("id") is None else result.first()
    if not res and exception:
        raise ObjectNotFoundError("Объект не найден")
    return res


async def get_or_404(
    model, id: int, asession: async_sessionmaker[AsyncSession] = async_session
):
    return await get(model, asession, exception=True, id=id)


async def get_all(model, asession: async_sessionmaker[AsyncSession] = async_session):
    return await get(model, asession)
