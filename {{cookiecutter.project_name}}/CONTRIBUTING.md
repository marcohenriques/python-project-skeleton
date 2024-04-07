# Contributing

## Setup

### Requirements

* Make:
    * MacOS: `$ xcode-select --install`
    * Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
* [Pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://poetry.eustace.io/docs/#installation) (version ~{{cookiecutter.poetry_version}})

To confirm these system dependencies are configured correctly:

```bash
./scripts/verchew
```

In Linux, make sure you have all required Python dependencies installed:
```shell
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev liblzma-dev tk-dev
```

### Installation

Before installing the project, make sure there's no python virtual environment active, as poetry will try to use it
to build the virtual environment. You can run:

```bash
deactivate
```

to deactivate the virtual environment.


Install project dependencies into a virtual environment:

```make
make install
```

Additional, the first time it runs, it will also:

* initialize git
* install _pre-commit_ in git hooks (this will run the hooks when you commit/push your changes)
* setup a default git message template for commits

## Development Tasks

### Manual

Run the tests:

```make
make test
```
(the first time it runs will also install the `tests` dependency group)

Read full coverage report:

```make
make read-coverage
```

Run formatters (_ruff_ and _sqlfluff_):

```make
make -k format
```

Run code static analysis (_ruff_, _mypy_, _sqlfluff_, _shellcheck_ and _safety_):

```make
make -k check
```

{% if cookiecutter.include_docs == "yes" -%}
Build and open/serve the documentation:

```make
make docs
```
(the first time it runs will also install the `docs` dependency group)

{% endif -%}
Run all _pre-commit_ hooks for all files:

```make
make pre-commit
```

Clean all temporary folder/files on the project:

```make
make clean
```

If you to also remove the virtual environment, run:

```make
make uninstall
```

{% if cookiecutter.include_notebooks == "yes" %}
Open jupyter notebooks on notebooks directory:

```make
make jupyter
```
(the first time it runs will also install the `jupyter` dependency group, and register an ipython kernel with the name
of the project)

{% endif -%}
### Continuous Integration

Run formatters, linters, tests{% if cookiecutter.include_docs == "yes" -%}, build documentation{% endif -%}:

```make
make -k ci
```

## Version control and commit message

For version control, consider follow the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.

Follow the pre-installed [git message template](./.gitmessage). The commit message should follow [the conventional commits](https://www.conventionalcommits.org). We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate it, there's also a pre-commit hooks to check at commit time.
