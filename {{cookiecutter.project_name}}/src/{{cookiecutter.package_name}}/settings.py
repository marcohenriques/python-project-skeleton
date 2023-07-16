"""Global project settings."""
from pathlib import Path
from typing import Optional

from pydantic import DirectoryPath, FilePath, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from python_package.constants import Environment


class AppSettings(BaseSettings):
    """Project settings.

    All values are can be read from environment variables, with the prefix `APP_`
    followed by the variable name (case sensitive).
    Pydantic will automatically convert the value to the correct type, or throw
    an error if the value is not valid.

    Check https://docs.pydantic.dev/latest/api/pydantic_settings/ for more info.

    Args:
        ENV (Environment): environment to use.
        PACKAGE_DIR (DirectoryPath): directory where the package is located.
        LOGGING_CONFIG (Optional[FilePath]): path to the logging configuration file.
    """

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)

    ENV: Environment = Environment.LOCAL
    PACKAGE_DIR: DirectoryPath = Path(__file__).parent
    LOGGING_CONFIG_PATH: Optional[FilePath] = None

    @field_validator("LOGGING_CONFIG_PATH")
    @classmethod
    def default_logging_config_path(
        cls,
        logging_config_path: Optional[FilePath],
        info: FieldValidationInfo,
    ) -> Optional[FilePath]:
        """Get the default logging config path if not provided.

        Args:
            logging_config_path (Optional[FilePath]): LOGGING_CONFIG_PATH value
            info (FieldValidationInfo): pydantic validation object (let you access other values)

        Returns:
            Optional[FilePath]: the default logging config path
        """
        if logging_config_path is None and "ENV" in info.data:
            env: Environment = info.data["ENV"]
            return Path(__file__).parent.parent / "configs" / env / "logging_config.yaml"
        return logging_config_path


settings = AppSettings()
