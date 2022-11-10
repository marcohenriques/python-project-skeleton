# Poetry

> Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your
project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable
installs, and can build your project for distribution.

The project uses <a href="https://python-poetry.org/" target="_blank"><code>poetry</code></a> to manage your
dependencies in a deterministic way, to make sure everyone uses the same dependencies versions (and the dependencies
of the dependencies).

## Dependency groups

The project organizes some dependencies into groups, so you don't need to install some groups of dependencies unless
they're required. The predefined groups of dependencies are:

- your core project dependencies
- `dev`: related to development tasks (formatter, linters, pre-commit)
- `tests`: to run tests
- `docs`: to build documentation
- `jupyter`: to run jupyter notebooks and formatter and linters for notebooks

To learn how to manage these groups, please refer to poetry <a href="https://python-poetry.org/docs/managing-dependencies/" target="_blank">dependency groups documentation</a>

## Basic usage

Here we describe some basic usage for poetry, for more details and additional available commands, please refer to the
<a href="https://python-poetry.org/docs/cli/" target="_blank">documentation</a>.

### Install dependencies

Install the required dependencies:

```bash
poetry install
```

If there's no `poetry.lock` Poetry simply resolves all dependencies listed in your `pyproject.toml` file and downloads
the latest version of their files. In the end, it will write the `poetry.lock`.  
If you already have a `poetry.lock` file, it will use this file to install the exact versions listed on it.

If you also want to install some optional dependency group, let's say `docs`, you should run:

```bash
poetry install --with docs
```

### Add new dependencies

If you want to add a new dependency to your core dependencies (let's say `django`), run:

```bash
poetry add django
```

This will find a suitable version constraint and install the package and sub-dependencies

If you add to add a dependency to a specific group (let's say `pytest` into `tests` group), run:

```bash
poetry add pytest --group tests
```

You can also specify a <a href="https://python-poetry.org/docs/dependency-specification#version-constraints" target="_blank">version constraint</a>:

```bash
poetry add django@4.0.0
```

In this case, poetry would install the exact specified `django` version.

For more options on how to add dependencies, please check the <a href="https://python-poetry.org/docs/dependency-specification" target="_blank">dependency specification documentation</a>.

### Update dependencies

To update all your dependencies, to the latest allowed versions (according to constraints), run:

```bash
poetry update
```

If you just want to update some dependencies (let's say `django` and `pytest`), run:

```bash
poetry django pytest
```

If you need to update a dependency outside the constraint defined in the `pyproject.toml`, you'll have to use the
`poetry add` command.

### Remove dependencies

To remove a dependency (let's say `django`), from your core dependency group run:

```bash
poetry remove django
```

If it's in other dependency group (let's say `pytest` into `tests` group), run:

```bash
poetry remove pytest --group tests
```

### Show package details

Poetry also allows you to check package details. To check all your required dependencies details run:

```bash
poetry show
```

If you also want some optional dependency groups (let's say `tests` group), run:

```bash
poetry show --with tests
```

For detailed information on a specific package (let's say `pytest`), run:

```bash
poetry show pytest
```

you'll see something like this:

```
 name         : pytest  
 version      : 7.2.0  
 description  : pytest: simple powerful testing with Python

dependencies
 - attrs >=19.2.0
 - colorama *
 - exceptiongroup >=1.0.0rc8
 - iniconfig *
 - packaging *
 - pluggy >=0.12,<2.0
 - tomli >=1.0.0

required by
 - pytest-clarity >=3.5.0
 - pytest-cookies >=3.3.0
 - pytest-cov >=4.6
```

### Running commands using your virtual environment

You can make sure you're running commands inside your project virtual environment in 2 ways:

```bash
poetry run <my_command>
```

This will execute `<my_command>` from your virtual environment, and return to the environment where you were running.

Or you can also run:

```{ .bash .annotate }
poetry shell # (1)
```

1.  Note that this command starts a new shell and activates the virtual environment.
<br><br>As such, `exit` should be used to properly exit the shell and the virtual environment instead of `deactivate`.

This spawns a shell, according to the `$SHELL` environment variable, within the virtual environment. Then you can run
your command inside the provisioned shell.
