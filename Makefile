# HELP ########################################################################
.DEFAULT_GOAL := help

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: help
help:
	@ printf "\nusage : make <commands> \n\nthe following commands are available : \n\n"
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e "s/^Makefile://" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# APP ########################################################################

# Project settings
PROJECT := python-project-skeleton
PACKAGE := hooks
PYTHON_VERSION=3.10

# Style makefile outputs
ECHO_COLOUR=\033[0;34m
NC=\033[0m # No Color

# Project paths
PACKAGES := $(PACKAGE) tests
MODULES := $(wildcard $(PACKAGE)/**/*.py)

# Virtual environment paths
VIRTUAL_ENV_NAME ?= .venv

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	${ROOT_DIR}/scripts/verchew --exit-code --root="${CURDIR}/scripts"

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES := $(VIRTUAL_ENV_NAME)/.poetry-$(shell ${ROOT_DIR}/scripts/checksum pyproject.toml poetry.lock)
TOOLS_FIRST_INSTALLED := $(VIRTUAL_ENV_NAME)/.tools_first_installed

.PHONY: install
install: $(DEPENDENCIES) $(TOOLS_FIRST_INSTALLED) .cache  ## Install project dependencies and tools


install-docs: $(TOOLS_FIRST_INSTALLED)_docs
$(TOOLS_FIRST_INSTALLED)_docs:
	poetry install --with docs --no-root
	@ touch $@

$(DEPENDENCIES): $(VIRTUAL_ENV_NAME)
	poetry install
	@ touch $@

$(TOOLS_FIRST_INSTALLED): .git
	@ poetry run pre-commit install -t pre-commit -t pre-push -t commit-msg
	@ poetry run git config commit.template .gitmessage
	@ touch $@ # This will create a file named `.tools_first_installed` inside venv folder

.git:
	git init

.cache:
	@ mkdir -p .cache

$(VIRTUAL_ENV_NAME): .python-version  ## Create python environment
	$(MAKE) doctor
	poetry env use -- $(shell pyenv which python)

.python-version:  # Setup .python-version (local pyenv python version) file
	@ echo "$(ECHO_COLOUR)Initializing pyenv$(NC)"
	$(eval PYENV_LATEST_VERSION=$(shell pyenv install --list | grep " $(PYTHON_VERSION)\.[0-9]*$$" | tail -1))
	@ echo "$(ECHO_COLOUR)Installing python version $(PYENV_LATEST_VERSION)...$(NC)"
	pyenv install -s $(PYENV_LATEST_VERSION)
	pyenv local $(PYENV_LATEST_VERSION)

requirements.txt: poetry.lock  ## Generate requirements.txt file from poetry
	@ echo "$(ECHO_COLOUR)Generating requirements.txt$(NC)"
	@ poetry export -f requirements.txt --without-hashes -o requirements.txt
	@ poetry run ${ROOT_DIR}/scripts/req_fixer requirements.txt

requirements-dev.txt: poetry.lock  ## Generate requirements.txt file from poetry
	@ echo "$(ECHO_COLOUR)Generating requirements.txt$(NC)"
	@ poetry export -f requirements.txt --without-hashes -o requirements-dev.txt --with dev,tests
	@ poetry run ${ROOT_DIR}/scripts/req_fixer requirements-dev.txt


# CHECKS ######################################################################

.PHONY: format
format:  ## Run formatters
	@ echo "$(ECHO_COLOUR)##### Running isort #####$(NC)"
	poetry run isort $(PACKAGES)
	@ echo "$(ECHO_COLOUR)##### Running black #####$(NC)"
	poetry run black $(PACKAGES)

.PHONY: check-packages
check-packages:  ## Run package check
	@ echo "$(ECHO_COLOUR)Checking packages$(NC)"
	poetry check
	poetry run pip check
	poetry export -f requirements.txt --without-hashes | poetry run safety check --full-report --stdin

mypy:
	@ echo "$(ECHO_COLOUR)##### Running mypy #####$(NC)"
	poetry run mypy --install-types --non-interactive $(PACKAGES)

flake8:
	@ echo "$(ECHO_COLOUR)##### Running flake8 #####$(NC)"
	poetry run flake8 $(PACKAGES)

.PHONY: lint
lint: mypy flake8 shellcheck  ## Run linters (mypy, flake8, shellcheck)

.PHONY: check
check: check-packages lint  ## Run linters, and static code analysis

.PHONY: bump
bump:  ## Bumps version number based on commit history
	poetry run cz bump -ch


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
test-all:
	@ if test -e $(FAILURES); then poetry run pytest $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	poetry run pytest $(PYTEST_OPTIONS)

.PHONY: read-coverage
read-coverage:  ## Open last coverage report in html page
	${ROOT_DIR}/scripts/open htmlcov/index.html


# DOCUMENTATION ###############################################################

MKDOCS_INDEX := site/index.html

.PHONY: build-docs
build-docs: install-docs $(MKDOCS_INDEX) ## Generate mkdocs documentation locally
$(MKDOCS_INDEX): mkdocs.yml docs/*.md
	poetry run mkdocs build --clean --strict

.PHONY: docs
docs: build-docs ## Serve the documentation (localhost:8000)
	eval "sleep 3; scripts/open http://127.0.0.1:8000" & poetry run mkdocs serve

.PHONY: mike-docs
mike-docs: build-docs ## Serve the documentation using mike (localhost:8000)
	eval "sleep 3; scripts/open http://127.0.0.1:8000" & poetry run mike serve -a 127.0.0.1:8000

.PHONY: deploy-docs
deploy-docs:  ## Deploys the documentation to github pages
	poetry run mike deploy -p $(cz version -p) latest


# CLEANUP #####################################################################

.PHONY: clean
clean: .clean-build .clean-docs .clean-test .clean-install ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean ## Delete virtual environment and all generated and temporary files
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


# OTHER TASKS #################################################################

.PHONY: all
all: install

.PHONY: ci
ci: format check test build-docs ## Run all tasks that determine CI status
