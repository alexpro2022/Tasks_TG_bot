from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import db_conf

engine = create_async_engine(db_conf.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
