"""Global project settings."""

from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Project settings.

    All values are can be read from environment variables, with the variable name (case sensitive).
    Pydantic will automatically convert the value to the correct type, or throw
    an error if the value is not valid.

    Check [pydantic_settings](https://docs.pydantic.dev/latest/api/pydantic_settings/)
    for more info.
    """

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)

    ENV: Literal["local", "dev", "prod"] = "local"
    "Environment to use"
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    "Name of the project"
    PACKAGE_DIR: DirectoryPath = Path(__file__).parent
    "Full path to the directory where the package is located"


settings = AppSettings()
logger.debug(f"Settings: {settings}")
