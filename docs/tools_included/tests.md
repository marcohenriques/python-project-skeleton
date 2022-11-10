# Tests

For testing, we use <a href="https://docs.pytest.org/" target="_blank"><code>pytest</code></a> with some predefined
configs (you can check it on `pyproject.toml` file). Additionaly, we're also packing pytest with some plugins:

- <a href="https://pytest-cov.readthedocs.io/en/latest/" target="_blank">pytest-cov</a>: produces coverage reports
- <a href="https://github.com/darrenburns/pytest-clarity" target="_blank">pytest-clarity</a>: coloured diff output
- <a href="https://github.com/pytest-dev/pytest-randomly" target="_blank">pytest-randomly</a>: randomly order tests and controls random.seed
- <a href="https://github.com/MobileDynasty/pytest-env" target="_blank">pytest-env</a>: enables you to set environment variables in the pytest config file
- <a href="https://github.com/Erotemic/xdoctest" target="_blank">xdoctest</a>: allows executing tests in docstrings
