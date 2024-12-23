# Contributing

- [Contributing](#contributing)
  - [Setup](#setup)
    - [Requirements](#requirements)
    - [Installation](#installation)
  - [Development Tasks](#development-tasks)
    - [Manual](#manual)
    - [Continuous Integration](#continuous-integration)
    - [Useful commands](#useful-commands)
      - [uv add/remove](#uv-addremove)
      - [uv run](#uv-run)
      - [uv tree](#uv-tree)
  - [Version control and commit message](#version-control-and-commit-message)
  - [Environment variables](#environment-variables)

## Setup

### Requirements

- Make:
  - MacOS: `$ xcode-select --install`
  - Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (version ~0.4.18)

To confirm these system dependencies are configured correctly:

```bash
make doctor
```

In Linux, make sure you have all required Python dependencies installed:

```shell
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev liblzma-dev tk-dev
```

### Installation

Install project dependencies into a virtual environment:

```make
make install
```

Additional, the first time it runs, it will also:

- initialize git
- install _pre-commit_ in git hooks (this will run the hooks when you commit/push your changes)
- setup a default git message template for commits
- install development dependencies and the python version selected (if not yet installed)

You can also run:

```make
make reinstall
```

to delete the virtual environment and temporary files and reinstall it again.

## Development Tasks

### Manual

To see all the make commands available run:

```make
make
```

Run the tests:

```make
make test
```

Read full coverage report:

```make
make read-coverage
```

Run formatters (_ruff_ and _sqlfluff_):

```make
make -k format
```

{% if cookiecutter.include_docs == "yes" -%}
Build and open/serve the documentation:

```make
make docs
```

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

{% if cookiecutter.include_notebooks == "yes" -%}
Open jupyter notebooks on notebooks directory:

```make
make jupyter
```

(the first time it runs it will register a local ipython kernel with the name of the project)

{% endif -%}
### Continuous Integration

Run formatters, linters, tests{% if cookiecutter.include_docs == "yes" -%}, build documentation{% endif -%}:

```make
make -k ci
```

### Useful commands

#### uv add/remove

To add/remove a dependency from your project dependencies you can run:

```bash
uv add django
uv remove django
```

If the dependency belongs to a group (eg. `dev`) you can use:

```bash
uv add --group dev pytest
uv remove --group dev pytest
```

#### uv run

Run a command/you application using your virtual environment:

```bash
uv run <my_command>
```

you can also run it using a environment file:

```bash
uv run <my_command> --env-file <my_env_file>
```

#### uv tree

Show package details:

```bash
uv tree
```

## Version control and commit message

For version control, consider follow the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.

Follow the pre-installed [git message template](./.gitmessage). The commit message should follow [the conventional commits](https://www.conventionalcommits.org). We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate it.

## Environment variables

The project comes with a `.env.template` file where you can find the relevant environment variables used in the project.
You should copy this file to `.env` and fill in/change the values. Alternatively, you can instead have a file by
environment (`.env.dev`, `.env.prod`, etc). You can execute the following command to export the environment variables:

```bash
export $(grep -v '^#' .env | xargs)
```
