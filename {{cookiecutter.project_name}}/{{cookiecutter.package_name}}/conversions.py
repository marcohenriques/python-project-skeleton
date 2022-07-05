"""This file serves only as example, it should be modified/removed."""

import logging

from {{cookiecutter.package_name}}.exceptions import TooBigFeetError


LOGGER = logging.getLogger(__name__)

METER_TO_FOOT_SCALE = 3.281


def feet_to_meters(feet: int) -> float:
    """Convert feet to meters.

    Args:
        feet (int): feet value

    Raises:
        ValueError: if failed to convert input to float
        TooBigFeetError: too big feet value

    Returns:
        float: feet value converted into meters
    """
    try:
        value_feet = float(feet)
    except ValueError:
        LOGGER.error("Unable to convert to float: {feet}".format(feet=feet))
        raise
    if value_feet > 100:
        raise TooBigFeetError("That's some big feet value")
    return value_feet / METER_TO_FOOT_SCALE


def meters_to_feet(meters: int) -> float:
    """Convert meters to feet.

    Args:
        meters (int): meters value

    Returns:
        float: feet value converted into meters

    Raises:
        ValueError: if failed to convert input to float

    Examples:
        We can put some examples, and pytest can run them as tests.

        >>> meters_to_feet(1)
        3.281
    """
    try:
        value_meters = float(meters)
    except ValueError:
        LOGGER.error("Unable to convert to float: {meters}".format(meters=meters))
        raise
    return METER_TO_FOOT_SCALE * value_meters
