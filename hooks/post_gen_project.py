#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("post_gen_project")

DOCS_SOURCES = "docs_sources"
GITIGNORE_TEMP_NAME = "gitignore"
ALL_TEMP_FOLDERS = [DOCS_SOURCES]
DOCS_FILES_BY_TOOL = {
    "mkdocs": ["advanced.md", "/mkdocs.yml", "images/", "about/", "reference/"],
    "sphinx": [
        "conf.py",
        "contributing.rst",
        "history.rst",
        "index.rst",
        "installation.rst",
        "make.bat",
        "Makefile",
        "readme.rst",
        "usage.rst",
    ],
}
DS_DIRS = [
    "src/{{cookiecutter.package_name}}/data/",
    "src/{{cookiecutter.package_name}}/features/",
    "src/{{cookiecutter.package_name}}/models/",
    "src/{{cookiecutter.package_name}}/visualization/",
    "data/",
    "models/",
    "references/",
    "reports/",
]
CLI_FILES = ["tests/test_cli.py"]
CLI_DIRS = ["src/{{cookiecutter.package_name}}/cli/"]
DOCKER_DIRS = ["docker/"]
DOCKER_INCLUDE = ["Dockerfile"]
DOCKER_EXCLUDE = ["Dockerfile_poetry"]


def move_docs_files(docs_tool, docs_files, docs_sources):
    if docs_tool == "no":
        return

    root = os.getcwd()
    docs = "docs"

    docs_tool_name = "mkdocs"

    # logger.info("Initializing docs for %s", docs_tool)
    if not os.path.exists(docs):
        os.mkdir(docs)

    for item in docs_files[docs_tool_name]:
        dst, name = (root, item[1:]) if item.startswith("/") else (docs, item)
        src_path = os.path.join(docs_sources, docs_tool_name, name)
        dst_path = os.path.join(dst, name)

        # logger.info("Moving %s to %s.", src_path, dst_path)
        if os.path.exists(dst_path):
            os.unlink(dst_path)

        os.rename(src_path, dst_path)


def rename_gitignore():
    os.rename(GITIGNORE_TEMP_NAME, ".gitignore")


def remove_temp_folders(temp_folders):
    for folder in temp_folders:
        #logger.info("Remove temporary folder: %s", folder)
        shutil.rmtree(folder)


def process_datascience_env(data_science_structure):
    if data_science_structure == "no":
        os.remove("Makefile_DS")
        remove_temp_folders(DS_DIRS)
    else:
        os.remove("Makefile_DS")
        print("on progress")


def process_cli(command_line_interface):
    if command_line_interface != "yes":
        for file in CLI_FILES:
            os.remove(file)
        remove_temp_folders(CLI_DIRS)

def process_docker(use_docker) -> None:
    """
    Remove the Dockerfile and Dockerfile.test if the user doesn't want to use Docker.
    """
    if use_docker == "no":
        for file in DOCKER_INCLUDE:
            os.remove(file)
    for file in DOCKER_EXCLUDE:
        os.remove(file)
    remove_temp_folders(DOCKER_DIRS)


if __name__ == "__main__":
    move_docs_files("{{cookiecutter.docs_tool}}", DOCS_FILES_BY_TOOL, DOCS_SOURCES)
    remove_temp_folders(ALL_TEMP_FOLDERS)
    rename_gitignore()
    process_datascience_env("{{cookiecutter.data_science_structure}}")
    process_cli("{{cookiecutter.command_line_interface}}")
    process_docker("{{cookiecutter.use_docker}}")
