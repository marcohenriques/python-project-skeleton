# Requirements

## Rendering project

To use this template the only requirement is [cookiecutter](https://github.com/cookiecutter/cookiecutter).

## Generated project

- [Make](https://www.gnu.org/software/make/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (version ~0.4.18)

In Linux, make sure you have all required Python dependencies installed:
```shell
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev liblzma-dev tk-dev
```

---

To confirm these system dependencies are configured correctly, on your project directory run:

```bash
make doctor
```

After running this, you should see something similar to:

```
Checking for Make...

$ make --version
GNU Make 3.81
✔ MATCHED: GNU Make

Checking for uv...

$ uv --version
uv 0.4.18 (7b55e9790 2024-10-01)
✔ MATCHED: 0.4

Results: ✔ ✔
```

If you have all the ✔ you're good to go.
