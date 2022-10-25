"""Sample integration test module using pytest-describe and expecter."""
from pathlib import Path

from typer.testing import CliRunner

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.cli import app


runner = CliRunner()


def test_app_help() -> None:
    cli_result = runner.invoke(app, [])
    assert cli_result.exit_code == 0
    assert "Usage: {{cookiecutter.package_name}} [OPTIONS] COMMAND [ARGS]..." in cli_result.stdout


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


def test_app_lands_reigns_command() -> None:
    cli_result = runner.invoke(app, ["lands", "reigns", "destroy", "some"])
    assert cli_result.exit_code == 0
    assert "Destroying reign: some" in cli_result.stdout

    cli_result = runner.invoke(app, ["lands", "reigns", "conquer", "some"])
    assert cli_result.exit_code == 0
    assert "Conquering reign: some" in cli_result.stdout


def test_app_lands_towns_command() -> None:
    cli_result = runner.invoke(app, ["lands", "towns", "burn", "some"])
    assert cli_result.exit_code == 0
    assert "Burning town: some" in cli_result.stdout

    cli_result = runner.invoke(app, ["lands", "towns", "found", "some"])
    assert cli_result.exit_code == 0
    assert "Founding town: some" in cli_result.stdout


def test_app_file_read_command(content_file: Path) -> None:
    cli_result = runner.invoke(app, ["files", "read", "--filename", str(content_file)])
    assert cli_result.exit_code == 0
    assert "my content" in cli_result.stdout


def test_app_file_write_command(tmp_path: Path) -> None:  # noqa: WPS218
    write_file_path = tmp_path / "write_file.txt"
    append_file_path = tmp_path / "append_file.txt"

    cli_result = runner.invoke(
        app,
        [
            "files",
            "write",
            "my content",
            "--filename",
            str(write_file_path),
            "--filename-append",
            str(append_file_path),
        ],
    )
    assert cli_result.exit_code == 0

    cli_result = runner.invoke(
        app,
        [
            "files",
            "write",
            "new content",
            "--filename",
            str(write_file_path),
            "--filename-append",
            str(append_file_path),
        ],
    )
    assert cli_result.exit_code == 0

    cli_result_write = runner.invoke(app, ["files", "read", "--filename", str(write_file_path)])
    assert "my content" not in cli_result_write.stdout
    assert "new content" in cli_result_write.stdout

    cli_result_append = runner.invoke(app, ["files", "read", "--filename", str(append_file_path)])
    assert "my content" in cli_result_append.stdout
    assert "new content" in cli_result_append.stdout
