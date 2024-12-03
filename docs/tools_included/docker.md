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

## Usage

To build it:

```make
make build-docker
```

To run it:

```make
make run-docker
```
