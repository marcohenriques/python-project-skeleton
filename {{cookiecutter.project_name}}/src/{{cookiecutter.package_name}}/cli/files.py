import time
from pathlib import Path
from typing import List, Optional

import typer


app = typer.Typer(
    name="files",
    no_args_is_help=True,
    short_help="files operations",
    help="This is the main help for files commands",
)


@app.command(no_args_is_help=True)
def check_exist(
    file_list: List[Path] = typer.Argument(
        None,
        metavar="object-list",
        help="list where to search the object",
    ),
    use_progressbar: bool = typer.Option(default=True, help="whether use progressbar"),
) -> None:
    """Check if list of files exist.

    Args:
        file_list (str): list of files to verify
        use_progressbar (bool): whether use progressbar. Defaults to True.
    """
    if use_progressbar:
        output = []
        with typer.progressbar(file_list, label="Verifying") as progress:
            for file_to_verify in progress:
                time.sleep(0.3)  # noqa: WPS432
                checker_icon = "✅" if file_to_verify.exists() else "❌"
                output.append(f"{checker_icon} {file_to_verify.absolute()}")
        typer.echo("\n".join(output))
    else:
        for file_to_verify in file_list:  # noqa: WPS440
            time.sleep(0.3)  # noqa: WPS432
            checker_icon = "✅" if file_to_verify.exists() else "❌"
            typer.echo(f"{checker_icon} {file_to_verify.absolute()}")


@app.command(no_args_is_help=True, help="create a file")
def write(
    text: str,
    filename: typer.FileTextWrite = typer.Option(..., help="file to write"),
    filename_append: typer.FileTextWrite = typer.Option(..., mode="a", help="file to append"),
) -> None:
    """Write text to file.

    Args:
        text (str): text to write
        filename (typer.FileTextWrite): file to write
        filename_append (typer.FileTextWrite): file to append
    """
    typer.echo(f"Writing '{text}' to {filename.name}")
    filename.write(text.encode().decode("unicode-escape"))
    typer.echo(f"Appending '{text}' to {filename_append.name}")
    filename_append.write(text.encode().decode("unicode-escape"))


@app.command(no_args_is_help=True, help="read a file")
def read(filename: typer.FileText = typer.Option(...)) -> None:
    """Read a file.

    Args:
        filename (typer.FileText): file to read
    """
    for line in filename:
        typer.echo(f"File line: {line}")


@app.command(help="checks on files and directories")
def check(config: Optional[Path] = typer.Option(None)) -> None:
    """Checks on files and directories.

    Args:
        config (Optional[Path]): config to check

    Raises:
        Abort: if config is none
    """
    typer.echo(f"Config file: {config}")
    if config is None:
        typer.echo("No config file")
        raise typer.Abort()
    if config.is_file():
        text = config.read_text()
        typer.echo(f"Config file contents: {text}")
    elif config.is_dir():
        typer.echo("Config is a directory, will use all its config files")
    elif not config.exists():
        typer.echo("The config doesn't exist")
