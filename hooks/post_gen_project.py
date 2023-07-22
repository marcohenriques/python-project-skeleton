"""Operations to perform after generating the project."""

import logging
import shutil
from pathlib import Path


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger("post_gen_project")


def process_docs(include_docs: str) -> None:
    """Process the docs.

    Args:
        include_docs (str): whether to include docs or not ('yes' or 'no')
    """
    logger.debug("Processing docs")
    if include_docs == "no":
        logger.info("Not including docs")
        shutil.rmtree("docs/")
        Path("mkdocs.yml").unlink()
        Path("readthedocs.yml").unlink(missing_ok=True)


def rename_gitignore() -> None:
    """Rename the gitignore file to .gitignore."""
    Path("gitignore").rename(".gitignore")


def process_cli(include_cli: str) -> None:
    """Process the CLI.

    Args:
        include_cli (str): whether to include CLI or not ('yes' or 'no')
    """
    logger.debug("Processing cli")
    if include_cli == "no":
        logger.info("Not including cli")
        shutil.rmtree("src/{{cookiecutter.package_name}}/cli/")
        Path("tests/test_cli.py").unlink()


def process_docker(include_docker: str) -> None:
    """Process the docker files.

    Args:
        include_docker (str): whether to include docker files or not ('yes' or 'no')
    """
    logger.debug("Processing docker")
    if include_docker == "no":
        logger.info("Not including docker")
        shutil.rmtree("docker/")
        Path("Dockerfile").unlink()
        Path(".dockerignore").unlink()
        Path(".github/workflows/build_docker.yaml").unlink()
    # optional dockerfile with poetry - not supported yet
    Path("Dockerfile_poetry").unlink()


if __name__ == "__main__":
    process_docs("{{cookiecutter.include_docs}}")
    rename_gitignore()
    process_cli("{{cookiecutter.include_cli}}")
    process_docker("{{cookiecutter.include_docker}}")
