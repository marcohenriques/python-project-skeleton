# Quickstart

Before we start generating our project, make sure you already have [everything](./requirements.md) needed.

## Generate project

Run the following command to create a new project, on your current directory:

```bash
cookiecutter gh:marcohenriques/python-project-skeleton
```

During this process you'll be prompted for several [inputs](./index.md#template-inputs) to configure your project.

## Setup new generated project

First, go to your project directory:

```bash
cd <my_project_name>
```

Then, to install all the dependencies just run:

```bash
make install
```

To make sure everything is ok, you can run:

```bash
make test
```

If all the tests passed without issues, you're good to go 🚀
