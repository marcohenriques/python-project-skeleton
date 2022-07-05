"""Test example using pytest. This file serves only as example, it should be modified/removed."""

import math

import pytest

from {{cookiecutter.package_name}} import conversions


@pytest.mark.parametrize(
    "value_feet,expected_value_meter",
    [
        (42, 12.800975312404754),
    ],
)
def test_describe_feet_to_meters_when_integer(value_feet: int, expected_value_meter: float):
    value_meter = conversions.feet_to_meters(value_feet)
    assert math.isclose(value_meter, expected_value_meter)


def test_describe_feet_to_meters_when_string():
    with pytest.raises(ValueError):
        conversions.feet_to_meters("hello")  # type: ignore
