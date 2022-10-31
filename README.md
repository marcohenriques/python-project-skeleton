# Python project skeleton

<a href="https://github.com/cookiecutter/cookiecutter">
  <img src="https://img.shields.io/badge/cookiecutter-template-D4AA00.svg?style=flat&logo=cookiecutter" alt="Cookiecutter template badge">
</a>
<br>

A cookiecutter template for python projects.

---

**Docs**: <a href="https://marcohenriques.github.io/python-project-skeleton" target="_blank">https://marcohenriques.github.io/python-project-skeleton</a>

**Code**: <a href="https://github.com/marcohenriques/python-project-skeleton" target="_blank">https://github.com/marcohenriques/python-project-skeleton</a>

---

### Features included

- Github actions CICD to run formatters, linter, tests. Also support to build and push docker images
- Dockerfile to ship python apps
- Documentation with [`mkdocs`](https://www.mkdocs.org/) using the beautiful [`material`](https://squidfunk.github.io/mkdocs-material/getting-started/) theme
- Testing using [`pytest`](https://docs.pytest.org/en/7.2.x/) and several plugins
- Code formatters using [`black`](https://black.readthedocs.io/en/stable/) and [`isort`](https://pycqa.github.io/isort/)
- Linters using [`flake8`](https://flake8.pycqa.org/en/latest/) (with [`wemake-python-styleguide`](https://wemake-python-styleguide.readthedocs.io/en/latest/)), [`mypy`](http://mypy-lang.org/) and [`shellcheck`](https://github.com/shellcheck-py/shellcheck-py)
- Python dependencies vulnerabilities scanner using [`safety`](https://github.com/pyupio/safety)
- [`pre-commit`](https://pre-commit.com/) hooks for some validations
- `Makefile` to automate some development tasks
- [`poetry`](https://python-poetry.org/) to manage your python dependencies
- Python package pre-configured with:
    - logging module to be easier to manage your loggers per environment
    - setting module using [`pydantic`](https://pydantic-docs.helpmanual.io/) to help manage your project settings
    - (optional) CLI example using [`typer`](https://typer.tiangolo.com/)

## Requirements

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/en/2.0.2/installation.html) installed.

## Installation

Run the following command to create a new project, on your current directory:

```bash
cookiecutter gh:marcohenriques/python-project-skeleton
```

## Template inputs

The template asks for the following inputs:

- `project_name`: The name of the project. This is used to name the project folder.
- `package_name`: The name of the package. This is used to name the package folder.
- `project_description`: A short description of the project.
- `author_name`: The name of the author.
- `author_email`: The email of the author.
- `github_username_or_org_name`: The github username or organization name.
- `python_version`: The python version to use.
- `include_docker`: Whether to include docker support.
- `include_notebooks`: Whether to include support for jupyter notebooks.
- `include_docs`: Whether to include support for documentation.
- `include_cli`: Whether to include support for a command line interface.
