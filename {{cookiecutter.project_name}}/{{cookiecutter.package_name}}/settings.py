import os
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, FilePath

from {{cookiecutter.package_name}}.constants import Environment


APP_ENV_PREFIX = "APP_"


class AppSettings(BaseSettings):
    """Project settings.

    All values are can be read from environment variables, with the prefix `APP_`
    followed by the variable name (case sensitive).
    Pydantic will automatically convert the value to the correct type, or throw
    an error if the value is not valid.

    Check https://pydantic-docs.helpmanual.io/usage/settings/ for more info.
    """

    ENV: Environment = Environment.DEV
    PACKAGE_DIR: DirectoryPath = Path(__file__).parent
    LOGGING_CONFIG_PATH: FilePath = (
        Path(__file__).parent
        / "configs"
        / os.getenv(f"{APP_ENV_PREFIX}ENV", Environment.DEV)
        / "logging_config.yaml"
    )

    class Config(object):  # noqa: WPS431
        """Config for Pydantic."""

        env_prefix = APP_ENV_PREFIX
        case_sensitive = True


settings = AppSettings()
