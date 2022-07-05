import os


PACKAGE_DIR = "/".join(__file__.split("/")[:-1])
CONFIGS_DIR = "configs"
ENVIRONMENT = os.getenv("APP_ENV", "dev")

LOGGING_CONFIG_FILENAME = "logging_config.yaml"
LOGGING_CONFIG_PATH = os.path.join(PACKAGE_DIR, CONFIGS_DIR, ENVIRONMENT, LOGGING_CONFIG_FILENAME)

METER_TO_FOOT_SCALE = 3.281
