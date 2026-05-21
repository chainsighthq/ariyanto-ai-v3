from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    EXECUTION_MODE: Literal["simulation", "live"] = "simulation"
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SQLITE_DB_PATH: str = "./data/ariyanto_ai.db"
    
    # Safety settings
    MAX_POSITION_SIZE_USD: float = 1000.0  # Max $1000 per trade in live mode
    REQUIRE_CONFIRMATION: bool = True      # Require confirmation for live trades
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
