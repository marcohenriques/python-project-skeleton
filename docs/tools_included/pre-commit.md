# <a href="https://pre-commit.com/" target="_blank"><code>pre-commit</code></a>

Having `pre-commit` hooks allows one to run different types of checks in different stages.

In this project, we're only installing by default hooks for `pre-commit`, `pre-push` and `commit-msg`. So if you want
to add other stages, please make sure to install them before. If you have any doubts you can always check the
<a href="https://pre-commit.com/" target="_blank">documentation</a>.

Following is a list with the included hooks:

- <a href="https://github.com/commitizen-tools/commitizen#integrating-with-pre-commit" target="_blank">commitizen</a>: hook to verify your commit message follows the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) (there's a `.gitmessage` template that is installed with your project that help you with that)
- <a href="https://github.com/pre-commit/pre-commit-hooks#requirements-txt-fixer" target="_blank">requirements-txt-fixer</a>: sorts entries in requirements.txt
- <a href="https://github.com/pre-commit/pre-commit-hooks#trailing-whitespace" target="_blank">trailing-whitespace</a>: remove any trailing whitespace (ignores line breaks in markdown files)
- <a href="https://github.com/pre-commit/pre-commit-hooks#end-of-file-fixer" target="_blank">end-of-file-fixer</a>: make sure all files ends with a new line
- <a href="https://github.com/pre-commit/pre-commit-hooks#check-yaml" target="_blank">check-yaml</a>: attempts to load all yaml files to verify syntax
- <a href="https://github.com/pre-commit/pre-commit-hooks#check-symlinks" target="_blank">check-symlinks</a>: checks for symlinks which do not point to anything
- <a href="https://github.com/pre-commit/pre-commit-hooks#check-toml" target="_blank">check-toml</a>: attempts to load all TOML files to verify syntax
- <a href="https://github.com/pre-commit/pre-commit-hooks#check-added-large-files" target="_blank">check-added-large-files</a>: prevent giant files from being committed (default: `1000kB`)
- <a href="https://github.com/asottile/add-trailing-comma#add-trailing-comma" target="_blank">add-trailing-comma</a>: add a trailing comma to python code when applicable
- **isort**: runs *isort* formatter
- **black**: runs *black* formatter
- **check-packages**: runs *safety check* linter
- **flake8**: runs *flake8* linter
- **mypy**: runs *mypy* type checker
- **shellcheck**: runs *shellcheck* linter
- **nbqa-isort**: runs *isort* on your jupyter notebooks, using *nbqa*. Only included if selected in the project setup (`include_notebooks`)
- **nbqa-black**: runs *black* on your jupyter notebooks, using *nbqa*. Only included if selected in the project setup (`include_notebooks`)
- **nbqa-flake8**: runs *flake8* on your jupyter notebooks, using *nbqa*. Only included if selected in the project setup (`include_notebooks`)
- **nbqa-mypy**: runs *mypy* on your jupyter notebooks, using *nbqa*. Only included if selected in the project setup (`include_notebooks`)
