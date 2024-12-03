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

- GitHub actions CICD to run formatters, linters, and tests. Also support to build and push docker images
- Dockerfile to ship python apps
- Documentation with <a href="https://www.mkdocs.org/" target="_blank"><code>mkdocs</code></a> using the beautiful
<a href="https://squidfunk.github.io/mkdocs-material/getting-started/" target="_blank"><code>material</code></a> theme
- Testing using <a href="https://docs.pytest.org/" target="_blank"><code>pytest</code></a> and several plugins
- Code formatters using <a href="https://beta.ruff.rs/docs/" target="_blank"><code>ruff</code></a> and
<a href="https://sqlfluff.com/" target="_blank"><code>sqlfluff</code></a> (SQL)
- Linters using <a href="https://beta.ruff.rs/docs/" target="_blank"><code>ruff</code></a>
(check configuration file for enabled plugins),
<a href="http://mypy-lang.org/" target="_blank"><code>mypy</code></a>,
<a href="https://github.com/shellcheck-py/shellcheck-py" target="_blank"><code>shellcheck</code></a> and
<a href="https://sqlfluff.com/" target="_blank"><code>sqlfluff</code></a>
- Python dependencies vulnerabilities scanner using <a href="https://github.com/pyupio/safety" target="_blank"><code>safety</code></a>
- Check for issues with dependencies with <a href="https://deptry.com/" target="_blank"><code>deptry</code></a>
- <a href="https://pre-commit.com/" target="_blank"><code>pre-commit</code></a> hooks for some validations
- `Makefile` to automate some development tasks
- <a href="https://docs.astral.sh/uv/" target="_blank"><code>uv</code></a> to manage your python versions and dependencies
- Python package pre-configured with:
  - logging using <a href="https://loguru.readthedocs.io/en/stable/" target="_blank"><code>loguru</code></a>
  - <a href="https://pydantic-docs.helpmanual.io/" target="_blank"><code>pydantic</code></a> to help manage your project settings
  - (optional) CLI example using <a href="https://typer.tiangolo.com/" target="_blank"><code>typer</code></a>

## Requirements

You'll need to have <a href="https://cookiecutter.readthedocs.io/en/2.0.2/installation.html" target="_blank">cookiecutter</a> and <a href="https://docs.astral.sh/uv/" target="_blank">uv</a> installed.

## Installation

Run the following command to create a new project on your current directory:

```bash
cookiecutter gh:marcohenriques/python-project-skeleton
```

If you want to use a different version of the template use the following command:

```bash
cookiecutter gh:marcohenriques/python-project-skeleton -c <VERSION>
```

where `<VERSION>` can be the branch, tag or commit of the template repo.

## Template inputs

The template asks for the following inputs:

- `project_name`: The name of the project. This is used to name the project folder.
- `package_name`: The name of the package. This is used to name the package folder.
- `project_description`: A short description of the project.
- `author_name`: The name of the author.
- `author_email`: The email of the author.
- `github_username_or_org_name`: The GitHub username or organization name.
- `python_version`: The python version to use.
- `include_docker`: Whether to include docker support.
- `include_notebooks`: Whether to include support for jupyter notebooks.
- `include_docs`: Whether to include support for documentation.
- `include_cli`: Whether to include support for a command line interface.
