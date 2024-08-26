import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_SERVER = os.getenv("PG_SERVER")
    PG_PORT = os.getenv("PG_PORT")
    PG_DB_NAME = os.getenv("PG_DB")
    PG_DB_URL = ("postgresql+psycopg2://"
                 f"{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB_NAME}")
