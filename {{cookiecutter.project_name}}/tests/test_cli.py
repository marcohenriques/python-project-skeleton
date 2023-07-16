"""Test examples for CLI. This file serves only as example, it should be modified/removed."""
from typer.testing import CliRunner

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.cli import app


runner = CliRunner()


def test_app_help() -> None:
    cli_result = runner.invoke(app, [])
    assert cli_result.exit_code == 0
    assert "{{cookiecutter.project_short_description}}" in cli_result.stdout


def test_app_version() -> None:
    cli_result = runner.invoke(
        app,
        ["--version", "simple-commands", "exit", "-vvvv", "--some-int", "3", "my_env_var_name"],
    )
    assert cli_result.exit_code == 0
    assert __version__ in cli_result.stdout


def test_app_simple_command() -> None:
    cli_result = runner.invoke(
        app,
        ["simple-command", "exit", "-vvvv", "--some-int", "3", "my_env_var_name"],
    )
    assert cli_result.exit_code == 0
    assert "some_field is 'exit'. Exiting with no error..." in cli_result.stdout

    cli_result = runner.invoke(app, ["fake-command"])
    assert cli_result.exit_code == 2
    assert "No such command 'fake-command'." in cli_result.stdout


def test_app_fake_command() -> None:
    cli_result = runner.invoke(app, ["fake-command"])
    assert cli_result.exit_code == 2
    assert "No such command 'fake-command'." in cli_result.stdout
