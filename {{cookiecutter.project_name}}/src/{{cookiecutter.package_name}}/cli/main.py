"""This file serves only as example, it should be modified/removed."""
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

import typer

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.settings import settings


class LogLevel(str, Enum):
    """Log level enum."""

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    WARNING = "WARNING"
    INFO = "INFO"  # noqa: WPS110
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


app = typer.Typer(
    name="{{cookiecutter.package_name}}",
    no_args_is_help=True,
    short_help="{{cookiecutter.package_name}} CLI",
    help="{{cookiecutter.project_short_description}}",
    pretty_exceptions_show_locals=False, # can be set to true for debugging
)


def version_callback(used_flag: bool) -> None:
    """Version callback.

    It terminates the program after printing the version.

    Args:
        used_flag (bool): whether the version flag was used

    Raises:
        Exit: if flag was used
    """
    if used_flag:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def app_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="print version",
    ),
) -> None:
    """App entry point.

    Args:
        version (Optional[bool]): print version.
    """


@app.command(name="simple-command", no_args_is_help=True)
def my_simple_command(  # noqa: WPS211, WPS213
    some_field: str,
    env_var_field: str = typer.Argument(..., envvar="ENV_VAR_FIELD"),
    some_int: int = typer.Option(1, min=1, max=3),
    some_cap_int: int = typer.Option(0, max=10, clamp=True),
    some_datetime: Optional[datetime] = typer.Option(None),
    some_uuid: uuid.UUID = typer.Option(uuid.uuid4),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
    log_level: LogLevel = typer.Option(LogLevel.WARNING),
) -> None:
    """Example command with different types.

    If not provided, this docstring will be automatically added to the `help` and `short_help`.

    Args:
        some_field (str): regular field
        env_var_field (str): regular field that can be overridden with an env var.
            Defaults to "default env_var_field" or "ENV_VAR_FIELD" if set.
        some_int (int): int value, must be between 1 and 3. Defaults to 1
        some_cap_int (int): int value, must be max 10, if above (with `clamp=True`),
            the value is set to the max. Defaults to 0
        some_datetime (Optional[datetime]): with datetime type, the string is automatically parsed.
            Defaults to None
        some_uuid (uuid.UUID): uuid field type. Defaults to a random uuid.uuid4
        verbose (int): with `count=True` the value is the number that the flags appears .
            Defaults to 0
        log_level (LogLevel): with enum types you can limit the accepted options.
            Defaults to LogLevel.WARNING

    Raises:
        Abort: if `some_field` is empty
        Exit: if `some_field` is "exit"
    """
    typer.echo("settings.ENV: {0}".format(settings.ENV))
    typer.echo("settings.PACKAGE_DIR: {0}".format(settings.PACKAGE_DIR))
    typer.echo("settings.LOGGING_CONFIG_PATH: {0}".format(settings.LOGGING_CONFIG_PATH))

    # Customize message with color and bold
    style_message = typer.style("Cool message", fg=typer.colors.GREEN, bold=True)
    typer.echo(style_message)

    # exiting execution with code 1 (abort) if some_field is empty
    if some_field == "":
        typer.echo("empty some_field. Exiting with error...")
        raise typer.Abort()

    # exiting execution with code 0 if some_field is "simple"
    if some_field == "exit":
        typer.echo("some_field is 'exit'. Exiting with no error...")
        raise typer.Exit()

    typer.echo(f"some_field: {some_field}")
    typer.echo(f"some_int: {some_int}")
    typer.echo(f"some_cap_int: {some_cap_int}")
    typer.echo(f"env_var_field: {env_var_field}")
    if some_datetime is None:
        some_datetime = datetime.now()
    typer.echo(f"some_datetime date: {some_datetime.date()} time: {some_datetime.time()}")
    typer.echo(f"some_uuid date: {some_uuid} (version {some_uuid.version})")
    typer.echo(f"Verbose level is {verbose}")
    typer.echo(f"log_level {log_level}")


if __name__ == "__main__":
    app()
