# Contributing

## Setup

### Requirements

* Make:
    * MacOS: `$ xcode-select --install`
    * Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
* [Pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://poetry.eustace.io/docs/#installation) (version ~{{cookiecutter.package_name}})

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

Run formatters (_black_ and _ruff_):

```make
make format
```

Run code static analysis (_ruff_,  _mypy_ and _safety_):

```make
make check
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

## Logging

For logging, we're using a centralized file (`logging_config.yaml`), under `{{ cookiecutter.project_name }}/src/configs/<your_environment>` (where _your\_environment_ is defined by the env var `APP_ENV`, defaults to **local**). In this file, you can define your log _formatters_, _filters_, _handlers_ and your _root_ and specific loggers (including from other packages). To better understand how to configure it, you can check the [logging-cookbook](https://docs.python.org/3/howto/logging-cookbook.html).

### Custom logging objects

We can define custom logging object to be used on our configurations file. To defined these object, the implementation should be in the `src/{{ cookiecutter.package_name }}/logging_setup.py` file to be properly loaded.

#### Handlers

For the native handlers please check [logging.handlers](https://docs.python.org/3/library/logging.handlers.html).

Other handler you might find useful is [watchtower](https://kislyuk.github.io/watchtower/#), which allows you send your logs to AWS CloudWatch Logs.

#### Filters

To define a custom filter you'll need to create a subclass of `logging.Filter` inside `{{ cookiecutter.package_name }}/logging_setup.py`. One example of a filter could be:

```python
class InfoFilter(logging.Filter):
    """Example of a simple logger filter, to only select logs with level INFO."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if the specified record is to be logged.

        Returns True if the record should be logged, or False otherwise.
        If deemed appropriate, the record may be modified in-place.

        Args:
            record (logging.LogRecord): log record

        Returns:
            bool: the filter predicate execution
        """
        return record.levelno == logging.INFO
```

Then to use the filter, on you `logging_config.yaml`, configure it like:

```yaml
formatters:
    standard:
        format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

filters:
    infoFilter:
        (): {{cookiecutter.package_name}}.logging_setup.InfoFilter

handlers:
    console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: standard
        stream: ext://sys.stdout

    cloudwatch:
        class: watchtower.CloudWatchLogHandler
        level: INFO
        formatter: standard
        log_group: /custom/apps/{{cookiecutter.package_name}}
        stream_name: app
        log_group_retention_days: 90

    info_file:
        class: logging.handlers.RotatingFileHandler
        level: INFO
        formatter: standard
        filename: /tmp/info.log
        maxBytes: 10485760
        backupCount: 20
        filters: [infoFilter] # example of a log filter
        encoding: utf8
```

In this case, the handler _info_file_ will only contains *INFO* logging records.

#### Loggers

**Note:** when defining loggers be mindful about the parameter [propagate](https://docs.python.org/3/library/logging.html#logging.Logger.propagate). As a rule of thumb, if you attach an handler to a logger, you will typically want to set this parameter to false, if not, the log record will be passed to the handlers of higher level (ancestor) loggers. For instances:

```yaml
root:
    level: NOTSET # if set, this will be the default logging level for all packages not cover in loggers section
    handlers: [console]
    propagate: no

loggers:
    {{cookiecutter.package_name}}:
        level: WARNING
        handlers: [console]
        propagate: no

    {{cookiecutter.package_name}}.some_package_a:
        level: DEBUG
        handlers: [info_file]
        propagate: no

    {{cookiecutter.package_name}}.some_package_b:
        level: DEBUG
        handlers: [info_file]

    {{cookiecutter.package_name}}.some_package_c:
        level: INFO

    {{cookiecutter.package_name}}.some_package_d:
        # level: NOTSET
        handlers: [info_file]
```

Lets see what's happening in there 4 last loggers:

- `{{cookiecutter.package_name}}.some_package_a`: log records are send only to *info_file* handler, with level **DEBUG**
- `{{cookiecutter.package_name}}.some_package_b`: log records are send to *info_file* and *console* (ancestor logger) handlers, with level **DEBUG**
- `{{cookiecutter.package_name}}.some_package_c`: log records are send only to *console* (ancestor logger) handler, with level **INFO**
- `{{cookiecutter.package_name}}.some_package_d`: log records are send to *info_file* and *console* (ancestor logger) handlers, with level **WARNING** (ancestor logger level)

## Version control and commit message

For version control, consider follow the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.

Follow the pre-installed [git message template](./.gitmessage). The commit message should follow [the conventional commits](https://www.conventionalcommits.org). We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate it, there's also a pre-commit hooks to check at commit time.


## IDE settings

### VS Code

To automatically leverage the linters and formatters from your vscode, you can add these configs to your
project `settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python3",
    "python.terminal.activateEnvironment": true,
    // Linters
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
    "python.linting.mypyArgs": [],
    // Formatters
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
    "python.formatting.blackArgs": [],
    // Tests
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "${workspaceFolder}/.venv/bin/pytest",
    "python.testing.pytestArgs": [],
}
```
