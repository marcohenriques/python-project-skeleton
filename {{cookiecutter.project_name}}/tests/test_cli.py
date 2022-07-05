"""Sample integration test module using pytest-describe and expecter."""
from click.testing import CliRunner

from {{cookiecutter.package_name}}.cli import main


def test_when_integer(runner: CliRunner):
    command_result = runner.invoke(main, ["option1", "42"])

    assert command_result.exit_code == 0
    assert command_result.output.split("\n")[1] == "12.800975312404754"
    assert len(command_result.output.split("\n")) == 4


def test_when_invalid_feet_value(runner: CliRunner):
    command_result = runner.invoke(main, ["option1", "foobar"])

    assert command_result.exit_code == 0
    assert len(command_result.output.split("\n")) == 3


def test_when_too_bg_feet_value(runner: CliRunner):
    command_result = runner.invoke(main, ["option1", "1000"])

    assert command_result.exit_code == 1


def test_with_home_directory(runner: CliRunner):
    command_result = runner.invoke(main, ["--home-directory=~", "option1", "foobar"])

    assert command_result.exit_code == 0
    assert command_result.output.split("\n")[0] == "My home directory is: ~"
    assert len(command_result.output.split("\n")) == 3
