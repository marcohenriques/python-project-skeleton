# GitHub Actions

The project bundles some workflows templates and some additional GitHub utils.

- `dependabot.yml`: to automatically check if your python dependencies and github actions are up to date
- `labeler.yml`: configuration to automatically add labels to your PR's based on the changed files
- workflows:
  - `build_docker.yaml`: template workflow to build and push images to [ghcr.io](https://github.com/features/packages)
  - `ci.yaml`: runs linters and tests
  - `main.yaml`: main cicd workflow
  - `pr-lint.yaml`: adds labels to your PR based on configuration and make sure PR title follows defined [convention](https://www.conventionalcommits.org/en/v1.0.0/)
