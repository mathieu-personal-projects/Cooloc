from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".docker/.env"

class Settings(BaseSettings):
    APP_NAME: str = "Cooloc's API"
    DEBUG: bool = False
    VERSION: str = "v2"
    API_PREFIX: str = "/api/" + VERSION

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()