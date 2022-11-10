# Docker

The project comes with a `Dockerfile` to helps containerize your application.

It already includes some best practices when building docker images, as such:

- <a href="https://docs.docker.com/build/building/multi-stage/" target="_blank">multi-stage building</a>: to better organize and optimize your build
- default non-root user when launching your container
- build from `python:<python_version>-slim` to keep your image small
- uses a `entrypoint` for your container
    - script in `docker/entrypoint.sh`, modify it according to your needs
    - entrypoint script is called with <a href="https://github.com/krallin/tini" target="_blank"><code>tini</code></a>
        - protects you from software that accidentally creates zombie processes
        - ensures that the default signal handlers work for the software you run in your Docker image

The `Dockerfile` uses 2 targets:

- `development`: image to use in development. With this you can mount a local volume that points to your code and if
you change it locally, it will automatically change in the container.
- `production`: image to use in production

When building both target, you'll need to have your project `requirements.txt` generated beforehand. You can do this running:

```{ .bash .annotate }
poetry export -f requirements.txt --without-hashes -o requirements.txt # (1)
```

1.  If you need additional dependency groups add the extra parameter `--with <your_other_group_1>,<your_other_group_2>`

For the `development` target, you'll also need your `requirements-dev.txt`, to generate this run:

```{ .bash .annotate }
poetry export -f requirements.txt --without-hashes -o requirements-dev.txt --with dev,tests # (1)
```

1.  If you need additional dependency groups add them like `--with dev,tests,<your_other_group>`

For the `production`, there's a Make target that will automatically build your image:

```make
make build-docker
```

And other to run it:

```make
make run-docker
```
