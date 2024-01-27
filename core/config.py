import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


# go to Pydantic Settings parser
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
MODE = os.environ.get('MODE')


class JwtAuthSettings(BaseModel):

    # Setings Authentication backends
    SECRET_KEY_BY_JWT: str
    SECRET_KEY_BY_UserManager: str 


class DbSettings(BaseModel):
    DB_USER: str = ...
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    echo: bool = False


# TODO: inherit pydantic BaseSettings
class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    jwt: JwtAuthSettings = JwtAuthSettings()


settings = Settings()
