import typer


app = typer.Typer(
    name="towns",
    no_args_is_help=True,
    short_help="towns operations",
    help="This is the main help for towns commands",
)


@app.command()
def found(name: str) -> None:
    """Finds a town.

    Args:
        name (str): town name
    """
    typer.echo(f"Founding town: {name}")


@app.command()
def burn(name: str) -> None:
    """Burns a town.

    Args:
        name (str): town name
    """
    typer.echo(f"Burning town: {name}")
