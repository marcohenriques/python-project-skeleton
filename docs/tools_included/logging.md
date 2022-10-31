## Logging

For logging, we're using a centralized file (`logging_config.yaml`), under `<my_project_name>/src/configs/<your_environment>` (where _your\_environment_ is defined by the env var `APP_ENV`, defaults to **local**). In this file, you can define your log _formatters_, _filters_, _handlers_ and your _root_ and specific loggers (including from other packages). To better understand how to configure it, you can check the [logging-cookbook](https://docs.python.org/3/howto/logging-cookbook.html).

### Custom logging objects

We can define custom logging object to be used on our configurations file. To defined these object, the implementation should be in the `src/<my_package_name>/logging_setup.py` file to be properly loaded.

#### Handlers

For the native handlers please check [logging.handlers](https://docs.python.org/3/library/logging.handlers.html).

Other handler you might find useful is [watchtower](https://kislyuk.github.io/watchtower/#), which allows you send your logs to AWS CloudWatch Logs.

#### Filters

To define a custom filter you'll need to create a subclass of `logging.Filter` inside `src/<my_package_name>/logging_setup.py`. One example of a filter could be:

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
        (): <my_package_name>.logging_setup.InfoFilter

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
        log_group: /custom/apps/<my_package_name>
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
    <my_package_name>:
        level: WARNING
        handlers: [console]
        propagate: no

    <my_package_name>.some_package_a:
        level: DEBUG
        handlers: [info_file]
        propagate: no

    <my_package_name>.some_package_b:
        level: DEBUG
        handlers: [info_file]

    <my_package_name>.some_package_c:
        level: INFO

    <my_package_name>.some_package_d:
        # level: NOTSET
        handlers: [info_file]
```

Lets see what's happening in there 4 last loggers:

- `<my_package_name>.some_package_a`: log records are send only to *info_file* handler, with level **DEBUG**
- `<my_package_name>.some_package_b`: log records are send to *info_file* and *console* (ancestor logger) handlers, with level **DEBUG**
- `<my_package_name>.some_package_c`: log records are send only to *console* (ancestor logger) handler, with level **INFO**
- `<my_package_name>.some_package_d`: log records are send to *info_file* and *console* (ancestor logger) handlers, with level **WARNING** (ancestor logger level)
