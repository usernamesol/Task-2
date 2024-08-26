from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dbase.db_conf import DBConfig


SQLALCHEMY_DATABASE_URL = DBConfig.PG_DB_URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(engine)


async def get_db() -> AsyncGenerator:
    try:
        db = SessionLocal()
        yield db
    finally:
        await db.close()
