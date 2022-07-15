"""Setup to load logging configuration file and additional logging formatters and filters."""

import logging
import os
from logging.config import dictConfig
from pathlib import Path
from typing import Optional

import yaml

from {{cookiecutter.package_name}}.settings import settings


LOGGER = logging.getLogger(__name__)
DEFAULT_LOGGING_LEVEL = logging.INFO


def setup_logging(
    logging_config_path: Optional[Path] = settings.LOGGING_CONFIG_PATH,
    default_level: int = DEFAULT_LOGGING_LEVEL,
) -> None:
    """Setup the logging.

    Args:
        logging_config_path (Optional[Path]): Path to configuration logging file.
            Defaults to LOGGING_CONFIG_PATH.
        default_level (int): Default logging level in case no config file found.
            Defaults to DEFAULT_LOGGING_LEVEL.
    """
    path = logging_config_path
    if path is not None and os.path.exists(path):
        with open(path, "rt") as config_file:
            try:
                config = yaml.safe_load(config_file.read())
                dictConfig(config)
            except Exception:
                LOGGER.error("Error in Logging config. Using default configs", stack_info=True)
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        LOGGER.error("Failed to load configuration file. Using default configs")


def get_logger(logger_name: str) -> logging.Logger:
    """Creates a logger object with `logger_name`.

    Args:
        logger_name (str): Logger name

    Returns:
        logging.Logger: Logger object
    """
    setup_logging()
    return logging.getLogger(logger_name)
