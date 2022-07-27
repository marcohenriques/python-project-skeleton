# Contributing

## Setup

### Requirements

* Make:
    * macOS: `$ xcode-select --install`
    * Linux: [https://www.gnu.org/software/make](https://www.gnu.org/software/make)
    * Windows: [https://mingw.org/download/installer](https://mingw.org/download/installer)
* Python: (`pyenv` or `conda`)
* Poetry: [https://poetry.eustace.io/docs/#installation](https://poetry.eustace.io/docs/#installation)

To confirm these system dependencies are configured correctly:

```bash
./scripts/verchew
```

### Installation

Install project dependencies into a virtual environment:

```make
make install
```

Additional, the first time it runs, it will also:

{% if cookiecutter.notebooks_support == "yes" -%}
* install _ipython kernel_ named `{{ cookiecutter.package_name }}`
{%- endif %}
* initialize git
* install _pre-commit_ in git hooks (this will run the hooks when you commit/push your changes)
* setup a default git message template for commits

## Development Tasks

### Manual

Run the tests:

```make
make test
```

Read full coverage report:

```make
make read-coverage
```

Run formatters (_black_ and _isort_):

```make
make format
```

Run code static analysis (_flake8_,  _mypy_ and _safety_):

```make
make check
```

{% if cookiecutter.docs_tool == "y" -%}
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

{% if cookiecutter.notebooks_support == "yes" %}
Open jupyter notebooks on notebooks directory (using configs in `notebooks/profile_default`):

```make
make jupyter
```

{% endif -%}
### Continuous Integration

Run formatters, linters, tests and build documentation:

```make
make ci
```

## Logging

For logging, we're using a centralized file (`logging_config.yaml`), under `{{ cookiecutter.package_name }}/configs/<your_environment>` (where _your\_environment_ is defined by the env var `APP_ENV`, defaults to **dev**). In this file, you can define your log _formatters_, _filters_, _handlers_ and your _root_ and specific loggers (including from other packages). To better understand how to configure it, you can check the [logging-cookbook](https://docs.python.org/3/howto/logging-cookbook.html).

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

## Version control

For version control, consider follow the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.  
Also try to follow the pre-installed git message template:

```
# A properly formed Git commit subject line should always be able to
# complete the following sentence:
#     * If applied, this commit <will your subject line here>

# ** Example template:
# [type](optional scope): [subject]
# |<----   Preferably using up to 50 chars   --->|<--- max 72 chars -->|
#
# [optional body]
#
# [optional footer]

# ** Example message:
# fix(parser): include correct price for shop X
#
# Use `price2` field to populate output `price` field.
#
# Shop X sometimes comes with empty `price` field, but with `price2`
# instead, now we pick `price2` whenever `price` field comes empty.
#
# Resolve: JIRA-1234

# ** Type
# Must be one of the following:
# * build - Build related changes
# * chore - Build process or auxiliary tool changes
# * docs - Documentation only changes
# * feat - A new feature
# * fix - A bug fix
# * perf - A code change that improves performance
# * refactor - A code change that neither fixes a bug or adds a feature
# * revert - Reverting things
# * style - Markup, white-space, formatting, missing semi-colons...
# * test - Adding missing tests

# ** Subject
# The subject contains a succinct description of the change:
# * Use the imperative, present tense: "change" not "changed" nor "changes"
# * No dot (.) at the end.

# ** Scope
# A scope may be provided to a commit’s type, to provide additional contextual information
# and is contained within parenthesis, e.g., feat(parser): add ability to parse arrays.

# ** Body
# Just as in the subject, use the imperative, present tense: "change" not "changed" nor "changes".
# The body should include the motivation for the change and contrast this with previous behavior.

# ** Footer
# Provide links or keys to any relevant tickets, articles or other resources.

# ** Rules
# The 7 rules of a great commit message
#    1. Separate subject from body with a blank line
#    2. Limit the subject line to 50 characters
#    3. Summary in present tense. Not capitalized
#    4. Do not end the subject line with a period
#    5. Use the imperative mood in the subject line
#    6. Wrap the body at 72 characters
#    7. Use the body to explain what and why vs. how
```

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
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Path": "${workspaceFolder}/.venv/bin/flake8",
    "python.linting.flake8Args": [],
    "python.linting.mypyEnabled": true,
    "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
    "python.linting.mypyArgs": [],
    // Formatters
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
    "python.formatting.blackArgs": [],
    "python.sortImports.path": "${workspaceFolder}/.venv/bin/isort",
    "python.sortImports.args": [],
    // Tests
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "${workspaceFolder}/.venv/bin/pytest",
    "python.testing.pytestArgs": [],
}
```
