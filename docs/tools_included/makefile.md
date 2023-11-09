# Makefile

The project includes a `Makefile` to help automate some tasks. These tasks can be grouped into sections.


## System Dependencies

To check if you have all the required tools:

```make
make doctor
```


## Project Dependencies

Tasks that help you set up your environment (create a virtual environment, install packages and tools...)

### install

```make
make install
```

This will should be the first command to prepare your environment. It will set up several things:

1. create a `.python-version` file, that will tell `pyenv` which python version to use. Behind the scenes, it will look
at the python version you select during project generation (which is stored in the variable `PYTHON_VERSION` on your
Makefile), and will search for the latest version available and use it (make sure to have `pyenv` up to date)

2. `poetry` will use this version and create your virtual environment on the project root (`.venv` folder), and then
install the project `core`, `dev` and `test` dependencies

3. if there's no git initialization in the project, it will perform a `git init`, if there is, it will be skipped

4. next, it will install the `pre-commit` hooks and install the git message template

### install-jupyter

```make
make install-jupyter
```

Install the dependencies to run jupyter notebooks. This target is only available if selected in the project setup
(`include_notebooks`).

### install-docs

```make
make install-docs
```

Install the dependencies to build documentation. This target is only available if selected in the project setup
(`include_docs`).

### requirements.txt

```make
make requirements.txt
```

This will update/generate the project `requirements.txt`, based on the installed dependencies from poetry.


## Checks

Tasks to run linters, formatters and python dependencies vulnerabilities scanner

### format

```make
make format
```

Runs all formatters: `sqlfluff` (SQL) and `ruff`(fix-only) on your **src** and *tests* directory.  
You can also run each check individually: `make format-sqlfluff` or `make format-ruff`.


### check-packages

```make
make check-packages
```

Runs checks on packages:
- Checks the validity of the `pyproject.toml` file
- Verify installed packages have compatible dependencies
- Run `safety check` to find vulnerabilities in Python dependencies

### lint

```make
make -k lint
```

Runs `sqlfluff`, `mypy` and `ruff` on your **src** and *tests* directory, and `shellcheck` on shell files.  
You can also run each check individually: `make lint-mypy`, `make lint-ruff` or `make lint-shellcheck`.

### check

```make
make -k check
```

Runs both `check-packages` and `lint` targets.

### pre-commit

```make
make pre-commit
```

Runs the pre-commit checks on all files.


## Tests

Tasks related to testing.

### test

```make
make test
```

Runs the tests with `pytest`. As we're using `pytest-randomly` to shuffle the tests, if the last run of the tests fails,
it will run the test with the same random seed first, and then, if the tests pass, it will run with a new one.

### read-coverage

```make
make read-coverage
```

Opens the coverage report for the last pytest run.


## Documentation

Tasks related to documentation. This section is only available if selected in the project setup (`include_docs`).

### build-docs

```make
make build-docs
```

Generate mkdocs documentation locally.  
The first this target is executed, it will run the target `install-docs` before.

### docs

```make
make docs
```

Build docs and serve them.


## Build

Tasks related to builds.

### dist

```make
make dist
```

Builds the package, as a tarball and a wheel.


## Cleanup

Tasks to clean up.

### clean

```make
make clean
```

Delete all generated and temporary files.

### clean-all

```make
make clean-all
```

Delete the virtual environment and all generated and temporary files.


## Docker

Tasks related to docker. This section is only available if selected in the project setup (`include_docker`).

### build-docker

```make
make build-docker
```

Build the docker image.

### run-docker

```make
make run-docker
```

Run the docker container for the built image.


## Other Tasks

### ci

```make
make -k ci
```

Run targets `format`, `check`, `test` and `build-docs` (if selected)

### jupyter

```make
make jupyter
```

Run jupyter notebooks on the notebooks directory (it will be created if it doesn't exist).  
The first this target is executed, it will run the target `install-jupyter` before.
