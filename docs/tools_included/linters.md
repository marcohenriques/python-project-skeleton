# Linters

## <a href="https://beta.ruff.rs/docs/" target="_blank"><code>ruff</code></a>

Linter for our python code.

This comes bundled with several plugins enabled. You can check them and respective configs on `pyproject.toml`.

For extra documentation on how to [add](https://beta.ruff.rs/docs/rules/) and/or [configure](https://beta.ruff.rs/docs/settings/) plugins, please see the ruff documentation.

## <a href="http://mypy-lang.org/" target="_blank"><code>mypy</code></a>

Used for static type checking in Python. The configurations are kinda strict, to enforce type annotations.

Check configs on `pyproject.toml`.

## <a href="https://github.com/shellcheck-py/shellcheck-py" target="_blank"><code>shellcheck</code></a>

Used to lint our shell scripts.
