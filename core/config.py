from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsApp(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore",
    )


class DbSettings(BaseSettingsApp):

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    MODE: str

    echo: bool = False

    @property
    def url(self):
        url: str = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url


class JwtAuthSettings(BaseSettingsApp):
    # Setings Authentication backends
    SECRET_KEY_BY_JWT: str
    SECRET_KEY_BY_UserManager: str


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    jwt: JwtAuthSettings = JwtAuthSettings()


settings = Settings()
