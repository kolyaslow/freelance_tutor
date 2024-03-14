from celery import Celery
from pydantic_settings import BaseSettings

from core.config import BaseSettingsApp


class Redis(BaseSettingsApp):
    REDIS_HOST: str
    REDIS_PORT: int


class EmailData(BaseSettingsApp):
    SENDER_EMAIL: str
    PASSWORD_EMAIL: str
    smtp_host: str = "smtp.mail.ru"
    port: int = 587


class Settings(BaseSettings):
    email: EmailData = EmailData()
    redis: Redis = Redis()


settings = Settings()
print(f"redis://{settings.redis.REDIS_HOST}:{settings.redis.REDIS_PORT}")
celery = Celery(
    "tasks", broker=f"redis://{settings.redis.REDIS_HOST}:{settings.redis.REDIS_PORT}"
)
