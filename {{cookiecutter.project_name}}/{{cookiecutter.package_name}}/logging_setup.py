"""Setup to load logging configuration file and additional logging formatters and filters."""

import logging
import os
from logging.config import dictConfig
from pathlib import Path

import yaml

from {{cookiecutter.package_name}}.settings import settings


LOG = logging.getLogger(__name__)
DEFAULT_LOGGING_LEVEL = logging.INFO
ENV_VAR_LOG_FILE = "LOG_CFG"


def setup_logging(
    default_path: Path = settings.LOGGING_CONFIG_PATH,
    default_level: int = DEFAULT_LOGGING_LEVEL,
    env_key: str = ENV_VAR_LOG_FILE,
) -> None:
    """Setup the logging.

    Args:
        default_path (Path): Path to configuration logging file.
            Defaults to LOGGING_CONFIG_PATH.
        default_level (int): Default logging level in case no config file found.
            Defaults to DEFAULT_LOGGING_LEVEL.
        env_key (str): Environment variable key name, which has the path to logging
            config. Defaults to ENV_VAR_LOG_FILE.
    """
    path = default_path
    env_value = os.getenv(env_key, None)
    if env_value:
        path = Path(env_value)
    if os.path.exists(path):
        with open(path, "rt") as config_file:
            try:
                config = yaml.safe_load(config_file.read())
                dictConfig(config)
            except Exception as error:
                LOG.error("Error in Logging Configuration. Using default configs")
                LOG.error(error)
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        LOG.error("Failed to load configuration file. Using default configs")


def get_logger(logger_name: str) -> logging.Logger:
    """Creates a logger object with `logger_name`.

    Args:
        logger_name (str): Logger name

    Returns:
        logging.Logger: Logger object
    """
    setup_logging()
    return logging.getLogger(logger_name)
