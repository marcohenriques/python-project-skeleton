"""Integration tests configuration file for pytest."""

import pytest
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()
    {%- endif %}
