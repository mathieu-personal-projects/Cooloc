from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Cooloc's API"
    DEBUG: bool = False
    VERSION: str = "v2"
    API_PREFIX: str = "/api/" + VERSION

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()