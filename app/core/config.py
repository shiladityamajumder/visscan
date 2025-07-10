# File: app/core/config.py
# Description: Configuration settings for the application using Pydantic's BaseSettings.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
