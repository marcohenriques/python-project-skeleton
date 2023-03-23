# HELP ########################################################################
.DEFAULT_GOAL := help

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Define macro to print which target is running
define INFO
    @echo "$(ECHO_COLOUR)##### Running$(NC) $1 $(ECHO_COLOUR)target #####$(NC)"
endef

# Store the macro call in a variable
PRINT_INFO = $(call INFO,$@)

.PHONY: help
help:
	@ printf "\nusage : make <commands> \n\nthe following commands are available : \n\n"
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e "s/^Makefile://" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# APP ########################################################################

# Project settings
PROJECT := {{cookiecutter.project_name}}
PACKAGE := src
PYTHON_VERSION={{ cookiecutter.python_version }}

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

{% if cookiecutter.include_docs == "yes" %}
install-docs: $(TOOLS_FIRST_INSTALLED)_docs
$(TOOLS_FIRST_INSTALLED)_docs:
	poetry install --with docs --no-root
	@ touch $@
{% endif %}{% if cookiecutter.include_notebooks == "yes" %}
install-jupyter: $(TOOLS_FIRST_INSTALLED)_jupyter
$(TOOLS_FIRST_INSTALLED)_jupyter:
	poetry install --with jupyter --no-root
	@ echo "$(ECHO_COLOUR)Creating ipython kernel$(NC)"
	@ poetry run python -m ipykernel install --sys-prefix --name {{ cookiecutter.package_name }}
	@ touch $@
{% endif %}
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
	$(PRINT_INFO)
	poetry run black $(PACKAGES)

.PHONY: check-packages
check-packages:  ## Run package check
	@ echo "$(ECHO_COLOUR)Checking packages$(NC)"
	poetry check
	poetry run pip check
	poetry export -f requirements.txt --without-hashes | poetry run safety check --full-report --stdin

mypy:
	$(PRINT_INFO)
	poetry run mypy --install-types --non-interactive $(PACKAGES)

ruff:
	$(PRINT_INFO)
	poetry run ruff --fix $(PACKAGES)

shellcheck:
	$(PRINT_INFO)
	@ $(eval sh_files := $(shell find . -not -path '*/.*' -regex '.*\.sh$$'))
	$(if $(sh_files),poetry run shellcheck $(sh_files), @ echo "No shell files found")

.PHONY: lint
lint: mypy ruff shellcheck  ## Run linters (mypy, ruff, shellcheck)

.PHONY: check
check: check-packages lint  ## Run linters, and static code analysis

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
test-all:
	@ if test -e $(FAILURES); then poetry run pytest $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	poetry run pytest $(PYTEST_OPTIONS)

.PHONY: read-coverage
read-coverage:  ## Open last coverage report in html page
	${ROOT_DIR}/scripts/open htmlcov/index.html
{% if cookiecutter.include_docs == "yes" %}

# DOCUMENTATION ###############################################################

MKDOCS_INDEX := site/index.html

.PHONY: build-docs
build-docs: install-docs $(MKDOCS_INDEX) ## Generate mkdocs documentation locally
$(MKDOCS_INDEX): mkdocs.yml docs/*.md
	poetry run mkdocs build --clean --strict

.PHONY: docs
docs: build-docs ## Serve the documentation (localhost:8000)
	eval "sleep 3; scripts/open http://127.0.0.1:8000" & poetry run mkdocs serve
{%- endif %}

# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl

.PHONY: dist
dist: install $(DIST_FILES)  ## Builds the package, as a tarball and a wheel
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

.PHONY: uninstall
uninstall: clean ## Delete virtual environment and all generated and temporary files
	rm -rf $(VIRTUAL_ENV_NAME)

.PHONY: clean
clean: .clean-build .clean-docs .clean-cache .clean-install ## Delete all generated and temporary files

.PHONY: .clean-install
.clean-install:
	find $(PACKAGES) -name '__pycache__' -delete
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

.PHONY: all
all: install

.PHONY: ci
ci: format check test {%- if cookiecutter.include_docs == "yes" %} build-docs{% endif %} ## Run all tasks that determine CI status
{% if cookiecutter.include_notebooks == "yes" -%}
notebooks:
	mkdir -p notebooks

.PHONY: jupyter
jupyter: install-jupyter notebooks ## Launch an Jupyter notebook session
	poetry run jupyter notebook --notebook-dir=notebooks
{% endif -%}
{% if cookiecutter.include_docker == "yes" %}

# DOCKER ######################################################################

DOCKER_IMAGE_NAME ?= {{cookiecutter.project_name.lower()}}
DOCKER_IMAGE_TAG ?= latest

.PHONY: build-docker
build-docker: requirements.txt  ## Build docker image
	docker build -f Dockerfile -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) --target production . --platform linux/amd64
	@ rm requirements.txt

.PHONY: run-docker
run-docker:  ## Run docker container for built image
	docker run -it --rm --platform linux/amd64 --name=$(DOCKER_IMAGE_NAME)_local $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
{% endif -%}
