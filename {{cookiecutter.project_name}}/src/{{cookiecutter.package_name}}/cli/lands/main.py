import typer

from {{cookiecutter.package_name}}.cli.lands import reigns, towns


app = typer.Typer(
    name="lands",
    no_args_is_help=True,
    short_help="lands operations",
    help="This is the main help for lands commands",
)
app.add_typer(reigns.app)
app.add_typer(towns.app)
