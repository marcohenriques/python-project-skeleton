# uv

> An extremely fast Python package and project manager, written in Rust.

The project uses <a href="https://docs.astral.sh/uv/" target="_blank"><code>uv</code></a> to manage your
dependencies in a deterministic way, to make sure everyone uses the same dependencies versions (and the dependencies
of the dependencies).

## Basic usage

Here we describe some basic commands for `uv`, for more details and additional available commands, please refer to the
<a href="https://docs.astral.sh/uv/reference/cli/" target="_blank">documentation</a>.

### Install dependencies

Install the required dependencies from `uv.lock` file:

```bash
uv sync --frozen
```

In case there's no `uv.lock` file or you want to update your `uv.lock` file with the latest dependencies
modifications in `pyproject.toml`, run:

```bash
uv sync
```

### Add new dependencies

If you want to add a new dependency to your core dependencies (let's say `django`), run:

```bash
uv add django
```

This will find a suitable version constraint and install the package and sub-dependencies.

If you add to add a dependency the dev dependencies (let's say `pytest`), run:

```bash
uv add --group dev pytest
```

You can also specify a version constraint:

```bash
uv add django==4.0.0
```

In this case, uv uv install the exact specified `django` version.

### Update dependencies

To update all your dependencies, to the latest allowed versions (according to constraints), run:

```bash
uv sync --upgrade
```

or a single one:

```bash
uv sync --upgrade-package <package>
```

or to specific version:

```bash
uv sync uv lock --upgrade-package <package>==<version>
```

### Remove dependencies

To remove a dependency (let's say `django`), from your core dependency group run:

```bash
uv remove django
```

If it's a dev dependency run:

```bash
uv remove --group dev pytest
```

### Show package details

Uv also allows you to check package details. To check all your required dependencies details run:

```bash
uv tree
```

### Running commands using your virtual environment

To make sure you're running commands inside your project virtual environment just use:

```bash
uv run <my_command>
```

This will execute `<my_command>` from your virtual environment, and return to the environment where you were running.
You can also run your command and pass the environment variables from a `.env` file:

```bash
uv run --env-file <my_dotenv> <my_command>
```
