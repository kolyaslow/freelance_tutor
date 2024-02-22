from core.config import BaseSettingsApp


class EmailData(BaseSettingsApp):
    SENDER_EMAIL: str
    PASSWORD_EMAIL: str
    smtp_host: str = "smtp.mail.ru"
    port: int = 587


email_data = EmailData()
