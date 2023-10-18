"""Global project settings."""

from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict

from {{cookiecutter.package_name}}.constants import Environment


class AppSettings(BaseSettings):
    """Project settings.

    All values are can be read from environment variables, with the prefix `APP_`
    followed by the variable name (case sensitive).
    Pydantic will automatically convert the value to the correct type, or throw
    an error if the value is not valid.

    Check [pydantic_settings](https://docs.pydantic.dev/latest/api/pydantic_settings/)
    for more info.

    Args:
        ENV (Environment): environment to use.
        PACKAGE_DIR (DirectoryPath): directory where the package is located.
    """

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)

    ENV: Environment = Environment.LOCAL
    PACKAGE_DIR: DirectoryPath = Path(__file__).parent


settings = AppSettings()
