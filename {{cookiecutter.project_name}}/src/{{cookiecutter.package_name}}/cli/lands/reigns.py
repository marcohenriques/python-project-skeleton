import typer


app = typer.Typer(
    name="reigns",
    no_args_is_help=True,
    short_help="reigns operations",
    help="This is the main help for reigns commands",
)


@app.command()
def conquer(name: str) -> None:
    """Conquers a reign.

    Args:
        name (str): reign name
    """
    typer.echo(f"Conquering reign: {name}")


@app.command()
def destroy(name: str) -> None:
    """Destroys a reign.

    Args:
        name (str): reign name
    """
    typer.echo(f"Destroying reign: {name}")
