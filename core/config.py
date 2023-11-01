import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')


class DbSettings(BaseModel):
    usl: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    echo: bool = False


class Settings():
    db: DbSettings = DbSettings()


settings = Settings()
