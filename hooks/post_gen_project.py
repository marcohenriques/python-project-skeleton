#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil


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
        os.remove("mkdocs.yml")
        # os.remove(".readthedocs.yml")


def rename_gitignore() -> None:
    """Rename the gitignore file to .gitignore."""
    os.rename("gitignore", ".gitignore")


def process_cli(include_cli: str) -> None:
    """Process the CLI.

    Args:
        include_cli (str): whether to include CLI or not ('yes' or 'no')
    """
    logger.debug("Processing cli")
    if include_cli == "no":
        logger.info("Not including cli")
        shutil.rmtree("src/{{cookiecutter.package_name}}/cli/")
        os.remove("tests/test_cli.py")


def process_docker(include_docker: str) -> None:
    """Process the docker files.

    Args:
        include_docker (str): whether to include docker files or not ('yes' or 'no')
    """
    logger.debug("Processing docker")
    if include_docker == "no":
        logger.info("Not including docker")
        shutil.rmtree("docker/")
        os.remove("Dockerfile")
        os.remove(".dockerignore")
        os.remove(".github/workflows/build_docker.yaml")
    # optional dockerfile with poetry - not supported yet
    os.remove("Dockerfile_poetry")


def _process_docker(include_docker: str) -> None:
    """Process the docker files.

    Args:
        include_docker (str): whether to include docker files or not ('yes' or 'no')
    """
    logger.debug("Processing docker")
    if include_docker == "no":
        logger.info("Not including docker")
        shutil.rmtree("docker/")
        os.remove("Dockerfile")
        os.remove(".dockerignore")
    # optional dockerfile with poetry - not supported yet
    os.remove("Dockerfile_poetry")


if __name__ == "__main__":
    process_docs("{{cookiecutter.include_docs}}")
    rename_gitignore()
    process_cli("{{cookiecutter.include_cli}}")
    process_docker("{{cookiecutter.include_docker}}")
