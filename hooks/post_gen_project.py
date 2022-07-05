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
    "{{cookiecutter.package_name}}/data/",
    "{{cookiecutter.package_name}}/features/",
    "{{cookiecutter.package_name}}/models/",
    "{{cookiecutter.package_name}}/visualization/",
    "data/",
    "models/",
    "references/",
    "reports/",
]
NB_DIRS = [
    "notebooks/",
]
CLICK_FILES = ["tests/test_cli.py"]
CLI_FILES = ["{{cookiecutter.package_name}}/cli.py"]


def move_docs_files(docs_tool, docs_files, docs_sources):
    if docs_tool == "none":
        return

    root = os.getcwd()
    docs = "docs"

    # logger.info("Initializing docs for %s", docs_tool)
    if not os.path.exists(docs):
        os.mkdir(docs)

    for item in docs_files[docs_tool]:
        dst, name = (root, item[1:]) if item.startswith("/") else (docs, item)
        src_path = os.path.join(docs_sources, docs_tool, name)
        dst_path = os.path.join(dst, name)

        # logger.info("Moving %s to %s.", src_path, dst_path)
        if os.path.exists(dst_path):
            os.unlink(dst_path)

        os.rename(src_path, dst_path)
    
    if docs_tool == "mkdocs":
        # Create symbolic links to readme, changelog and contributing
        os.symlink("../README.md", "docs/index.md")
        os.symlink("../../CHANGELOG.md", "docs/about/changelog.md")
        os.symlink("../../CONTRIBUTING.md", "docs/about/contributing.md")


def rename_gitignore():
    os.rename(GITIGNORE_TEMP_NAME, ".gitignore")


def remove_temp_folders(temp_folders):
    for folder in temp_folders:
        #logger.info("Remove temporary folder: %s", folder)
        shutil.rmtree(folder)


def process_datascience_env(processQ):
    if processQ == "no":
        os.remove("Makefile_DS")
        remove_temp_folders(DS_DIRS)
    else:
        os.remove("Makefile_DS")
        print("on progress")


def process_notebooks(processQ):
    if processQ == "no":
        remove_temp_folders(NB_DIRS)


def process_cli(cli_tool):
    if cli_tool != "Click":
        for file in CLICK_FILES:
            os.remove(file)
    if cli_tool == "none":
        for file in CLI_FILES:
            os.remove(file)


if __name__ == "__main__":
    move_docs_files("{{cookiecutter.docs_tool}}", DOCS_FILES_BY_TOOL, DOCS_SOURCES)
    remove_temp_folders(ALL_TEMP_FOLDERS)
    rename_gitignore()
    process_datascience_env("{{cookiecutter.data_science_structure}}")
    process_notebooks("{{cookiecutter.notebooks_support}}")
    process_cli("{{cookiecutter.command_line_interface}}")
