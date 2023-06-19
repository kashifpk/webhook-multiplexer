from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings, Field, validator

from . import PROJECT_ROOT


class Settings(BaseSettings):

    class Config:
        env_file = PROJECT_ROOT / ".env"

    app_name: str = "Nebra Helium Solana API"

    environment: str = Field(env='ENVIRONMENT')
    middleware_secret_key: str = Field(env='MIDDLEWARE_SECRET_KEY')
    auth_token: str = Field(env='AUTH_TOKEN')
    data_file: Path = Field(env='DATA_FILE')

    @validator("data_file", pre=True)
    def data_file_path(cls, v: bool | None, values: dict) -> Path:
        return PROJECT_ROOT / v

    debug: bool = False

    @validator("debug", pre=True)
    def determine_debug_mode(cls, v: bool | None, values: dict) -> bool:
        if isinstance(v, bool):
            return v

        if values['environment'] == 'development':
            return True

        return False



@lru_cache
def get_settings():
    return Settings()
