# COMMON ######################################################################
.DEFAULT_GOAL := help

# Project settings
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PROJECT := python-project-skeleton
PYTHON_VERSION=3.13

PACKAGE := hooks
DEV_PACKAGES := $(PACKAGE) tests
MODULES := $(wildcard $(PACKAGE)/**/*.py)

# Virtual environment paths
VIRTUAL_ENV_NAME ?= .venv

# Style makefile outputs
ECHO_COLOUR=\033[0;34m
NC=\033[0m # No Color

# Define macro to print which target is running
define INFO
    @echo "$(ECHO_COLOUR)##### Running $1 target #####$(NC)"
endef

# Store the macro call in a variable
PRINT_INFO = $(call INFO,$@)

.PHONY: help
help:
	@ printf "\nusage : make <commands> \n\nthe following commands are available : \n\n"
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e "s/^Makefile://" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	@ uvx verchew --exit-code --root="${CURDIR}/scripts"


# PROJECT DEPENDENCIES ########################################################

.PHONY: install
install: .cache uv.lock install-git-hooks  ## Install project dependencies and tools
	@ uv python pin $(PYTHON_VERSION)
	@ uv sync --frozen

install-git-hooks: .git .git/hooks/pre-commit .git/hooks/pre-push .git/hooks/commit-msg

.git/hooks/pre-commit .git/hooks/pre-push .git/hooks/commit-msg:
	@ uv run pre-commit install

.git:
	@ git init

.cache:
	@ mkdir -p .cache

uv.lock:
	@ uv lock

requirements.txt: uv.lock  ## Generate requirements.txt
	@ echo "$(ECHO_COLOUR)Generating $@$(NC)"
	@ uv export --frozen --no-dev --no-emit-project --all-extras --no-hashes -o $@

requirements-dev.txt: uv.lock  ## Generate requirements.txt
	@ echo "$(ECHO_COLOUR)Generating $@$(NC)"
	@ uv export --frozen --only-dev --no-emit-project --no-hashes -o $@


# CHECKS ######################################################################

format-ruff:
	$(PRINT_INFO)
	uv run ruff format --config ${ROOT_DIR}/pyproject.toml $(DEV_PACKAGES)
	uv run ruff check --config ${ROOT_DIR}/pyproject.toml --fix-only $(DEV_PACKAGES)

format-sqlfluff:
	$(PRINT_INFO)
	uv run sqlfluff fix --config ${ROOT_DIR}/pyproject.toml $(DEV_PACKAGES)

.PHONY: format
format: format-ruff format-sqlfluff  ## Run formatters (ruff, sqlfluff)

.PHONY: check-packages
check-packages:  ## Run package check
	@ echo "$(ECHO_COLOUR)Checking packages$(NC)"
	uv lock --locked -q
	uv export --frozen --no-dev --no-emit-project --no-hashes | uv run safety check --full-report --stdin
	uv run deptry $(PACKAGE)

lint-mypy:
	$(PRINT_INFO)
	uv run mypy --config-file ${ROOT_DIR}/pyproject.toml $(DEV_PACKAGES)

lint-ruff:
	$(PRINT_INFO)
	uv run ruff check --config ${ROOT_DIR}/pyproject.toml --no-fix $(DEV_PACKAGES)
	uv run ruff format --config ${ROOT_DIR}/pyproject.toml --check $(DEV_PACKAGES)

lint-shellcheck:
	$(PRINT_INFO)
	@ $(eval sh_files := $(shell find . -not -path '*/.*' -regex '.*\.sh$$'))
	$(if $(sh_files),uv run shellcheck $(sh_files), @ echo "No shell files found")

lint-sqlfluff:
	$(PRINT_INFO)
	uv run sqlfluff lint --config ${ROOT_DIR}/pyproject.toml $(DEV_PACKAGES)

.PHONY: lint
lint: lint-mypy lint-ruff lint-shellcheck lint-sqlfluff  ## Run linters (mypy, ruff, shellcheck, sqlfluff)

.PHONY: pre-commit
pre-commit:  ## Run pre-commit on all files
	uv run pre-commit run --all-files


# TESTS #######################################################################

RANDOM_SEED ?= $(shell date +%s)
FAILURES := .cache/v/cache/lastfailed

PYTEST_OPTIONS := --randomly-seed=$(RANDOM_SEED)

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
	@ if test -e $(FAILURES); then uv run pytest $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	uv run pytest $(PYTEST_OPTIONS)

.PHONY: read-coverage
read-coverage:  ## Open last coverage report in html page
	open htmlcov/index.html


# DOCUMENTATION ###############################################################

MKDOCS_INDEX := site/index.html

.PHONY: build-docs
build-docs: $(MKDOCS_INDEX)  ## Generate mkdocs documentation locally
$(MKDOCS_INDEX): mkdocs.yml docs/*.md src/**/*.py
	uv run mkdocs build --clean --strict

.PHONY: docs
docs: build-docs  ## Serve the documentation (localhost:8000)
	eval "sleep 3; open http://127.0.0.1:8000" & uv run mkdocs serve

.PHONY: mike-docs
mike-docs: build-docs ## Serve the documentation using mike (localhost:8000)
	eval "sleep 3; scripts/open http://127.0.0.1:8000" & uv run mike serve -a 127.0.0.1:8000

.PHONY: deploy-docs
deploy-docs:  ## Deploys the documentation to github pages
	uv run mike deploy -u -p $$(uv run cz version -p  | awk -F '.' '{ print $$1 "." $$2 }') latest
	uv run mike set-default -p latest


# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl

.PHONY: dist
dist: install $(DIST_FILES)  ## Builds the package, as a tarball and a wheel
$(DIST_FILES): $(MODULES) pyproject.toml
	rm -f $(DIST_FILES)
	uv build


# CLEANUP #####################################################################

.PHONY: uninstall
uninstall: clean  ## Delete virtual environment and all generated and temporary files
	rm -rf $(VIRTUAL_ENV_NAME)

.PHONY: clean
clean: .clean-build .clean-docs .clean-cache .clean-install  ## Delete all generated and temporary files

.PHONY: .clean-install
.clean-install:
	find $(DEV_PACKAGES) -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-cache
.clean-cache:
	rm -rf .cache .ruff_cache .mypy_cache .pytest .coverage htmlcov

.PHONY: .clean-docs
.clean-docs:
	rm -rf site

.PHONY: .clean-build
.clean-build:
	rm -rf *.spec dist build


# OTHER TASKS #################################################################

.PHONY: ci
ci: format check-packages lint test build-docs ## Run all tasks that determine CI status

.PHONY: bump
bump:  ## Bumps version number based on commit history
	uv run cz bump -ch
