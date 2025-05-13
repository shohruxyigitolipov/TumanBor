import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
load_dotenv('.env')

DATABASE_URL = os.getenv("DATABASE_URL")


class LoggingSettings(BaseSettings):
    telegram_enabled: bool = True
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    level: str = "INFO"
    log_to_console: bool = True
    log_to_file: bool = False
    log_file_path: str = "logs/app.log"
    max_bytes: int = 5 * 1024 * 1024
    backup_count: int = 3
    formatter: str = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
    telegram_formatter: str = "[%(levelname)s] %(name)s:%(lineno)d\n%(message)s"
    model_config = SettingsConfigDict(
        env_file=".env",              # путь до вашего .env
        env_file_encoding="utf-8",    # кодировка .env
        extra='ignore'
    )
