from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, DirectoryPath, FilePath, validator

from {{cookiecutter.package_name}}.constants import Environment


APP_ENV_PREFIX = "APP_"


class AppSettings(BaseSettings):
    """Project settings.

    All values are can be read from environment variables, with the prefix `APP_`
    followed by the variable name (case sensitive).
    Pydantic will automatically convert the value to the correct type, or throw
    an error if the value is not valid.

    Check https://pydantic-docs.helpmanual.io/usage/settings/ for more info.

    Args:
        ENV (Environment): environment to use.
        PACKAGE_DIR (DirectoryPath): directory where the package is located.
        LOGGING_CONFIG (Optional[FilePath]): path to the logging configuration file.
    """

    ENV: Environment = Environment.LOCAL
    PACKAGE_DIR: DirectoryPath = Path(__file__).parent
    LOGGING_CONFIG_PATH: Optional[FilePath] = None

    class Config(object):  # noqa: WPS431
        """Config for Pydantic."""

        env_prefix = APP_ENV_PREFIX
        case_sensitive = True

    @validator("LOGGING_CONFIG_PATH")
    def default_logging_config_path(
        cls,  # noqa: N805
        logging_config_path: Optional[FilePath],
        values: Dict[str, Any],  # noqa: WPS110
    ) -> Optional[FilePath]:
        """Get the default logging config path if not provided.

        Args:
            logging_config_path (Optional[FilePath]): LOGGING_CONFIG_PATH value
            values (Dict[str, Any]): previous provided class values

        Returns:
            Optional[FilePath]: the default logging config path
        """
        if logging_config_path is None and "ENV" in values:
            return Path(__file__).parent.parent / "configs" / values["ENV"] / "logging_config.yaml"
        return logging_config_path


settings = AppSettings()
