SHELL:=/usr/bin/env bash

# HELP ########################################################################
.DEFAULT_GOAL := help

.PHONY: help
help:
	@ printf "\nusage : make <commands> \n\nthe following commands are available : \n\n"
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e "s/^Makefile://" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# APP ########################################################################

# Project settings
PROJECT := {{cookiecutter.project_name}}
PACKAGE := {{cookiecutter.package_name}}
PYTHON_VERSION={{ cookiecutter.python_version }}

# Style makefile outputs
ECHO_COLOUR=\033[0;34m
NC=\033[0m # No Color

# Project paths
PACKAGES := $(PACKAGE) tests
CONFIG := $(wildcard *.py)
MODULES := $(wildcard $(PACKAGE)/*.py)

# Virtual environment paths
VIRTUAL_ENV_NAME ?= .venv

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	scripts/verchew --exit-code --root="${CURDIR}/scripts"

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES := $(VIRTUAL_ENV_NAME)/.poetry-$(shell scripts/checksum pyproject.toml poetry.lock)
TOOLS_FIRST_INSTALLED := $(VIRTUAL_ENV_NAME)/.tools_first_installed

.PHONY: install
install: $(DEPENDENCIES) $(TOOLS_FIRST_INSTALLED) .cache

$(DEPENDENCIES): $(VIRTUAL_ENV_NAME)
	poetry install
	@ touch $@
	@ $(MAKE) gen-req

$(TOOLS_FIRST_INSTALLED):
	{% if cookiecutter.notebooks_support == "yes" -%}
	@ echo "$(ECHO_COLOUR)Creating ipython kernel$(NC)"
	@ poetry run python -m ipykernel install --sys-prefix --name {{ cookiecutter.package_name }}
	{%- endif %}
	git init
	@ poetry run pre-commit install
	@ poetry run git config commit.template .gitmessage
	@ touch $@ # This will create a file named `.tools_first_installed` inside venv folder

.cache:
	@ mkdir -p .cache

{% if cookiecutter.python_version_management == "pyenv" -%}
$(VIRTUAL_ENV_NAME): ## Create python environment
	$(MAKE) doctor
	@ echo "$(ECHO_COLOUR)Initializing pyenv$(NC)"
	$(eval PYENV_LATEST_VERSION=$(shell pyenv install --list | grep " $(PYTHON_VERSION)\.[0-9]*$$" | tail -1))
	@ echo "$(ECHO_COLOUR)Installing python version $(PYENV_LATEST_VERSION)...$(NC)"
	pyenv install -s $(PYENV_LATEST_VERSION)
	pyenv local $(PYENV_LATEST_VERSION)
	poetry env use -- $(shell pyenv which python)
{%- elif cookiecutter.python_version_management == "conda" -%}
$(VIRTUAL_ENV_NAME): ## Create python environment
	$(MAKE) doctor
	conda create -y -p $(VIRTUAL_ENV_NAME) python=$(PYTHON_VERSION)
{%- endif %}

.PHONY: gen-req
gen-req:  ## Generate requirements files from poetry
	@ echo "$(ECHO_COLOUR)Updating requirements files$(NC)"
	@ poetry export -f requirements.txt --without-hashes -o requirements.txt
	@ poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt
	@ poetry run scripts/req_fixer requirements.txt requirements-dev.txt


# CHECKS ######################################################################

.PHONY: format
format:  ## Run formatters
	poetry run isort $(PACKAGES)
	poetry run black $(PACKAGES)
	@ echo

.PHONY: check
check:  ## Run linters, and static code analysis
	poetry check
	poetry run pip check
	poetry run safety check -r requirements.txt
	@ echo
	poetry run mypy --install-types --non-interactive $(PACKAGES)
	@ echo
	poetry run flake8 $(PACKAGES)

.PHONY: pre-commit
pre-commit:  ## Run pre-commit on all files
	poetry run pre-commit run --all-files


# TESTS #######################################################################

RANDOM_SEED ?= $(shell date +%s)
FAILURES := .cache/v/cache/lastfailed

PYTEST_OPTIONS := -v --cov=$(PACKAGE) --randomly-seed=$(RANDOM_SEED)

ifdef EXTRA_ARG
PYTEST_OPTIONS += $(EXTRA_ARG)
endif
ifdef DEBUG
PYTEST_OPTIONS += --pdb
endif

PYTEST_RERUN_OPTIONS := -v --randomly-seed=last

.PHONY: test
test: test-all ## Run unit and integration tests

.PHONY: test-all
test-all: install
	@ if test -e $(FAILURES); then poetry run pytest $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	poetry run pytest $(PYTEST_OPTIONS)

.PHONY: read-coverage
read-coverage:  ## Open last coverage report in html page
	scripts/open htmlcov/index.html


# DOCUMENTATION ###############################################################

{% if cookiecutter.docs_tool == "sphinx" -%}
.PHONY: build-docs
build-docs: install ## Generate Sphinx documentation locally
	rm -f docs/{{ cookiecutter.package_name }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.package_name }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs: build-docs ## Open the documentation
	scripts/open docs/_build/html/index.html
{%- elif cookiecutter.docs_tool == "y" -%}
MKDOCS_INDEX := site/index.html

.PHONY: build-docs
build-docs: install $(MKDOCS_INDEX) ## Generate mkdocs documentation locally
$(MKDOCS_INDEX): mkdocs.yml docs/*.md
	@ mkdir -p docs/about
	@ cd docs && ln -sf ../README.md index.md
	@ cd docs/about && ln -sf ../../CHANGELOG.md changelog.md
	@ cd docs/about && ln -sf ../../CONTRIBUTING.md contributing.md
	poetry run mkdocs build --clean --strict

.PHONY: docs
docs: build-docs ## Serve the documentation (localhost:8000)
	eval "sleep 3; scripts/open http://127.0.0.1:8000" & poetry run mkdocs serve
{%- endif %}

# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl

.PHONY: dist
dist: install $(DIST_FILES)
$(DIST_FILES): $(MODULES) pyproject.toml
	rm -f $(DIST_FILES)
	poetry build


# RELEASE #####################################################################

# .PHONY: upload
# upload: dist ## Upload the current version to PyPI
# 	git diff --name-only --exit-code
# 	poetry publish
# 	scripts/open https://pypi.org/project/$(PROJECT)


# CLEANUP #####################################################################

.PHONY: clean
clean: .clean-build .clean-docs .clean-test .clean-install ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean
	rm -rf $(VIRTUAL_ENV_NAME)

.PHONY: .clean-install
.clean-install:
	find $(PACKAGES) -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-test
.clean-test:
	rm -rf .cache .pytest .coverage htmlcov

.PHONY: .clean-docs
.clean-docs:
	rm -rf site

.PHONY: .clean-build
.clean-build:
	rm -rf *.spec dist build


# MAIN TASKS ##################################################################

.PHONY: all
all: install

.PHONY: ci
ci: format check test {%- if cookiecutter.docs_tool == "y" %} build-docs{% endif %} ## Run all tasks that determine CI status

{% if cookiecutter.notebooks_support == "yes" -%}
.PHONY: jupyter
jupyter: install ## Launch an Jupyter notebook session
	poetry run jupyter notebook --notebook-dir=notebooks
{% endif -%}
