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
* initialise git
* install _pre-commit_ in git hooks (this will run the hooks when you commit/push your changes)
* setup a default git message template for commits

## Development Tasks

### Manual

Run the tests:

```make
make test
```

Read full converage report:

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
Open jupyter notebooks on notebooks diretory (using configs in `notebooks/profile_default`):

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

For logging, we're using a centralised file (`logging_config.yaml`), under `{{ cookiecutter.package_name }}/configs/<your_environment>` (where _your\_environment_ is defined by the env var `APP_ENV`, defaults to **dev**). In this file, you can define your log _formatters_, _filters_, _handlers_ and your _root_ and specific loggers (including from other packages). To better understand how to configure it, you can check the [logging-cookbook](https://docs.python.org/3/howto/logging-cookbook.html).

### Custom logging objects

We can define custom logging object to be used on our configurations file. To defined these object, the implementation should be in the `{{ cookiecutter.package_name }}/logging_setup.py` file to be properly loaded.

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
# run `git config commit.template .gitmessage` to set this template as default
# [<tag>] (If applied, this commit will...) <subject> (Max 72 char)
# |<----   Preferably using up to 50 chars   --->|<------------------->|
# Example:
# [feat] Implement automated commit messages


# (Optional) Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# (Optional) Provide links or keys to any relevant tickets, articles or other resources
# Example: JIRA issue #23

# --- COMMIT END ---
# Tag can be
#    feat     (new feature)
#    fix      (bug fix)
#    refactor (refactoring code)
#    style    (formatting, missing semi colons, etc; no code change)
#    doc      (changes to documentation)
#    test     (adding or refactoring tests; no production code change)
#    version  (version bump/new release; no production code change)
#    deps     (app dependencies updates)
#    dbg      (Changes in debugging code/frameworks; no production code change)
#    hack     (Temporary fix to make things move forward; please avoid it)
#    WIP      (Work In Progress; for intermediate commits to keep patches reasonably sized)
#    defaults (changes default options)
#    configs  (changes in project configurations)
#
# Note: Multiple tags can be combined, e.g. [fix][deps] Fix issue X with new dependency version
# --------------------
# Remember to:
#   * Capitalize the subject line
#   * Use the imperative mood in the subject line
#   * Do not end the subject line with a period
#   * Separate subject from body with a blank line
#   * Use the body to explain what and why vs. how
#   * Can use multiple lines with "-" or "*" for bullet points in body
# --------------------
```
