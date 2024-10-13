"""Operations to perform after generating the project."""

import logging
import shutil
import subprocess
from pathlib import Path


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger("post_gen_project")


PROJECT_DEPENDENCIES = [
    "loguru",
    "pydantic",
    "pydantic-settings",
]

if "{{cookiecutter.include_cli}}" == "yes":  # type: ignore # noqa: PLR0133
    PROJECT_DEPENDENCIES.append("typer")


DEV_DEPENDENCIES = [
    # format and lint
    "ruff",
    "mypy",
    "safety>=2,<3",
    "pre-commit",
    "shellcheck-py",
    "sqlfluff",
    "deptry",
    # tests
    "pytest",
    "pytest-cov",
    "pytest-clarity",
    "pytest-randomly",
    "pytest-env",
    "xdoctest",
]


DOCS_DEPENDENCIES = [
    "mike",
    "mkdocs-gen-files",
    "mkdocs-literate-nav",
    "mkdocs-material",
    "mkdocs-section-index",
    "mkdocs",
    "mkdocstrings[python]",
]

if "{{cookiecutter.include_docs}}" == "yes":  # type: ignore # noqa: PLR0133
    DEV_DEPENDENCIES.extend(DOCS_DEPENDENCIES)

JUPYTER_DEPENDENCIES = [
    "jupyterlab",
]

if "{{cookiecutter.include_notebooks}}" == "yes":  # type: ignore # noqa: PLR0133
    DEV_DEPENDENCIES.extend(JUPYTER_DEPENDENCIES)


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


def install_dependencies() -> None:
    """Install the dependencies."""
    logger.debug("Installing dependencies")
    # setup python version to use
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "make",
            "uv.lock",
            "install",
        ],
        check=False,
    )
    # project dependencies
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "add",
            "--no-sync",
            *PROJECT_DEPENDENCIES,
        ],
        check=False,
    )
    # dev dependencies
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "add",
            "--no-sync",
            "--dev",
            *DEV_DEPENDENCIES,
        ],
        check=False,
    )


if __name__ == "__main__":
    process_docs("{{cookiecutter.include_docs}}")
    process_cli("{{cookiecutter.include_cli}}")
    process_docker("{{cookiecutter.include_docker}}")
    install_dependencies()
