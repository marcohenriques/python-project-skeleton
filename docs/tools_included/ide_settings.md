# IDE Settings

When you generate the project, the project will generate config file(s) to help set up your IDE to use some
development tool.

## VSCode

A `settings.json` file will be generated:

``` json title=".vscode/settings.json"
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python3",
  "python.terminal.activateEnvironment": true,
  // Linters/formatters
  "ruff.path": [
    "${workspaceFolder}/.venv/bin/ruff"
  ],
  "ruff.lint.args": [
    "--config=${workspaceFolder}/pyproject.toml"
  ],
  "ruff.format.args": [
    "--config=${workspaceFolder}/pyproject.toml"
  ],
  "mypy-type-checker.args": [
    "--config-file=${workspaceFolder}/pyproject.toml"
  ],
  "sqlfluff.config": "${workspaceFolder}/pyproject.toml",
  "sqlfluff.executablePath": "${workspaceFolder}/.venv/bin/sqlfluff",
  // Tests
  "python.testing.pytestEnabled": true,
  "python.testing.pytestPath": "${workspaceFolder}/.venv/bin/pytest",
  "python.testing.pytestArgs": [],
  // Vertical lines num characters
  "editor.rulers": [
    120
  ],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": true
    },
    "editor.rulers": [
      {
        "column": 80,
        "color": "#40824c38"
      },
      {
        "column": 100,
        "color": "#80808067"
      },
      {
        "column": 120,
        "color": "#ff010168"
      },
    ]
  },
  "[jsonc]": {
    "editor.rulers": []
  },
  "[git-commit]": {
    "editor.rulers": [
      50,
      72
    ]
  },
  "[markdown]": {
    "editor.rulers": [
      120,
    ]
  },
  "files.associations": {
    ".gitmessage": "git-commit",
    "*.toml": "toml",
  },
}
```

This is can be useful as it will automatically set up linters, formatters and tests to give you feedback inline. It'll
also set up your python interpreter to use the environment created by `poetry`, and automatically activate this
environment when you open a new shell.

If you already have your setup and don't want to use these settings, feel free to modify/delete them.

As this file can vary from developer to developer, depending on the extensions and customizations each wants per
project, this file is added on the `.gitignore`, so it will only be available/generated upon project creation.
