from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Literal
from loguru import logger

class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Execution
    EXECUTION_MODE: Literal["simulation", "live"] = "simulation"
    MAX_POSITION_SIZE_USD: float = 500.0
    REQUIRE_CONFIRMATION: bool = True

    # Infrastructure
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SQLITE_DB_PATH: str = "./data/ariyanto_ai.db"

    # Security
    ALLOWED_SOURCES: list = ["telegram", "cli", "internal"]

    @field_validator("EXECUTION_MODE")
    @classmethod
    def warn_live_mode(cls, v: str) -> str:
        if v == "live":
            logger.warning("⚠️  LIVE TRADING MODE ENABLED — Real money at risk!")
        return v

settings = Settings()
