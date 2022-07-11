import typer


app = typer.Typer(
    name="users",
    no_args_is_help=True,
    short_help="users operations",
    help="This is the main help for users commands",
)


def check_nickname_exists_callback(nickname: str) -> str:
    """Check if nickname exists callback.

    It terminates the program if nickname exists.

    Args:
        nickname (str): nickname to check.

    Raises:
        Abort: if nickname name exists

    Returns:
        str: capital nickname
    """
    if nickname in {"user1", "user2"}:
        typer.echo("Nickname already exists")
        raise typer.Abort()
    return nickname.upper()


@app.command(help="create a user", no_args_is_help=True)
def create(
    nickname: str = typer.Argument(..., callback=check_nickname_exists_callback),
    user_name: str = typer.Option(..., prompt=True),
    lastname: str = typer.Option(..., prompt="Now the lastname"),
) -> None:
    """Create a user.

    Args:
        nickname (str): nickname. Use callback to check if nickname already exists.
        user_name (str): user name. If not provided, it will be prompted.
        lastname (str): lastname. If not provided, it will be prompted.
    """
    typer.echo(f"Creating user: {nickname}")
    typer.echo(f"Creating user: {user_name} {lastname} ({nickname})")


@app.command()
def delete(
    user_name: str = typer.Option(..., prompt=True, confirmation_prompt=True),
    confirmation: bool = typer.Option(..., prompt="Are you sure?"),
) -> None:
    """Delete a user.

    Args:
        user_name (str): user name. If not provided, it will be prompted.
        confirmation (bool): confirmation. If not provided, it will be prompted.
    """
    if confirmation:
        typer.echo(f"Deleting user: {user_name}")
    else:
        typer.echo(f"User '{user_name}' not deleted")
