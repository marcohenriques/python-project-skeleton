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

JUPYTER_DEPENDENCIES = [
    "jupyterlab",
]


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
        Path("src/{{cookiecutter.package_name}}/cli.py").unlink()
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
    logger.debug("Setting up python version")
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "lock",
        ],
        capture_output=True,
        check=True,
    )
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "python",
            "pin",
            "{{cookiecutter.python_version}}",
        ],
        capture_output=True,
        check=True,
    )

    # project dependencies
    logger.debug("Adding base project dependencies")
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "add",
            "--no-sync",
            *PROJECT_DEPENDENCIES,
        ],
        capture_output=True,
        check=True,
    )
    # dev dependencies
    logger.debug("Adding dev dependencies")
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "add",
            "--no-sync",
            "--group",
            "dev",
            *DEV_DEPENDENCIES,
        ],
        capture_output=True,
        check=True,
    )
    # docs dependencies
    if "{{cookiecutter.include_docs}}" == "yes":  # type: ignore # noqa: PLR0133
        logger.debug("Adding docs dependencies")
        subprocess.run(  # noqa: S603
            [  # noqa: S607
                "uv",
                "add",
                "--no-sync",
                "--group",
                "docs",
                *DOCS_DEPENDENCIES,
            ],
            capture_output=True,
            check=True,
        )
    # jupyter dependencies
    if "{{cookiecutter.include_notebooks}}" == "yes":  # type: ignore # noqa: PLR0133
        logger.debug("Adding jupyter dependencies")
        subprocess.run(  # noqa: S603
            [  # noqa: S607
                "uv",
                "add",
                "--no-sync",
                "--group",
                "jupyter",
                *JUPYTER_DEPENDENCIES,
            ],
            capture_output=True,
            check=True,
        )


if __name__ == "__main__":
    process_docs("{{cookiecutter.include_docs}}")
    process_cli("{{cookiecutter.include_cli}}")
    process_docker("{{cookiecutter.include_docker}}")
    install_dependencies()
