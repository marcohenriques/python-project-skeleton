"""A sample CLI. This file serves only as example, it should be modified/removed."""

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}

import argparse
{%- endif %}
import logging
import sys
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from os import listdir
from typing import IO, Any, Optional

import click
{%- endif %}

from {{cookiecutter.package_name}} import conversions


LOGGER = logging.getLogger(__name__)

{%- if cookiecutter.command_line_interface|lower == 'click' %}


# You can find how to call it in pyproject.toml[tool.poetry.scripts]
@click.group()
@click.option("--verbose", is_flag=True)
@click.option("--home-directory", type=click.Path(), default=".")
def main(verbose: bool, home_directory: str) -> None:
    """Example of a simple cli."""
    home_files = listdir(home_directory)
    click.echo("My home directory has these files: {home_files}".format(home_files=home_files))


@click.command()
@click.option("--string", default="World", help="The thing greeted")
@click.option("--repeat", default=1, help="How many time to greet")
@click.argument("feet")
@click.argument("out", type=click.File("w"), default="-", required=False)
def option1(string: str, repeat: int, feet: int, out: Optional[IO[Any]]) -> None:
    """First option group."""
    try:
        meters = conversions.feet_to_meters(feet)
    except ValueError:
        LOGGER.info("Just ignoring")
    else:
        click.echo(meters)
    for _ in range(repeat):
        click.echo("Hello {string}".format(string=string), file=out)


# Add the command to our CLI
main.add_command(option1)
{%- elif cookiecutter.command_line_interface|lower == 'argparse' %}


def main():
    """Console script for {{cookiecutter.package_name}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    LOGGER.info("Arguments: " + str(args._))
    LOGGER.info("Replace this message by putting your code into "
          "{{cookiecutter.package_name}}.cli.main")
    return 0
{%- endif %}


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
