# Requirements

## Rendering project

To use this template the only requirement is [cookiecutter](https://github.com/cookiecutter/cookiecutter).

## Generated project

- [Make](https://www.gnu.org/software/make/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Poetry](https://poetry.eustace.io/docs/#installation) (version ~1.2.0)

In Linux, make sure you have all required Python dependencies installed:
```shell
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev liblzma-dev tk-dev
```

---

To confirm these system dependencies are configured correctly, on your project directory run:

```bash
./scripts/verchew
```
