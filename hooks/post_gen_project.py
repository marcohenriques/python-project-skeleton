#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger("post_gen_project")


def process_docs(include_docs: str) -> None:
    logger.debug("Processing docs")
    if include_docs == "no":
        logger.info("Not including docs")
        shutil.rmtree("docs/")
        os.remove("mkdocs.yml")
        # os.remove(".readthedocs.yml")


def rename_gitignore() -> None:
    os.rename("gitignore", ".gitignore")


def process_cli(include_cli: str) -> None:
    logger.debug("Processing cli")
    if include_cli == "no":
        logger.info("Not including cli")
        shutil.rmtree("src/{{cookiecutter.package_name}}/cli/")
        os.remove("tests/test_cli.py")


def process_docker(include_docker) -> None:
    """
    Remove the Dockerfile and Dockerfile.test if the user doesn't want to use Docker.
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
