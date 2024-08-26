from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbase.db_conf import DBConfig


SQLALCHEMY_DATABASE_URL = DBConfig.DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
