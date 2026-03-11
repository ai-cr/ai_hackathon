"""Configuration module for loading environment variables."""

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    gemini_api_key: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config() -> Config:
    """Load and return the application configuration."""
    return Config()