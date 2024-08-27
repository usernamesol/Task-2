import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_SERVER = os.getenv("PG_SERVER")
    PG_PORT = os.getenv("PG_PORT")
    PG_DB_NAME = os.getenv("PG_DB_NAME")
    PG_TEST_DB_NAME = os.getenv("PG_TEST_DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    PG_DB_URL = (
        "postgresql+asyncpg://"
        f"{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB_NAME}"
    )
    PG_TEST_DB_URL = (
        "postgresql+asyncpg://"
        f"{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_TEST_DB_NAME}"
    )
