import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SERVER = os.getenv("SERVER")
    PORT = os.getenv("PORT")
    DB = os.getenv("DB")
    DB_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"
