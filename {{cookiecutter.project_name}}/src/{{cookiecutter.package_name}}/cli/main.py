"""Main CLI definition."""

from typing import Optional

import typer

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.settings import settings


app = typer.Typer(
    name="{{cookiecutter.package_name}}",
    no_args_is_help=True,
    short_help="{{cookiecutter.package_name}} CLI",
    help="{{cookiecutter.project_short_description}}",
    pretty_exceptions_show_locals=False,  # can be set to true for debugging
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
    version: Optional[bool] = typer.Option(  # noqa: UP007, ARG001
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


@app.command(name="say-hello", no_args_is_help=True)
def run(name: str) -> None:
    """Prints hello message.

    If not provided, this docstring will be automatically added to the `help` and `short_help`.
    """
    # exiting execution with code 1 (abort) if name is empty
    if name == "":
        typer.echo("empty name. Exiting with error...")
        raise typer.Abort()

    # exiting execution with code 0 if name is "exit"
    if name == "exit":
        typer.echo("name is 'exit'. Exiting with no error...")
        raise typer.Exit()

    style_message = typer.style(f"Hello {name}", fg=typer.colors.GREEN, bold=True)
    typer.echo(style_message + f" (from {settings.ENV} environment)")


if __name__ == "__main__":
    app()
