# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:{{ cookiecutter.python_version }}-slim as python-base

# Needed for fixing permissions of files created by Docker
ARG UID=9999
ARG GID=9999

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    procps \
    build-essential \
    gcc \
    # Create custom user and group to run the app as:
    && groupadd -g "${GID}" -r web \
    && useradd -d /app -g web -l -r -u "${UID}" web \
    && chown web:web -R /app

COPY requirements.txt /
RUN pip install -U pip \
    && pip install -r /requirements.txt


# # 'production' stage uses the clean 'python-base' stage and copyies
# # in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production

COPY . .

# Add our app code to python path:
ENV PYTHONPATH="/app/src"

# Running as non-root user:
USER web

CMD ["python"]


# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development

COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt

# Instead of copying the whole project, we could mount a volume to current directory:
# COPY . .

# Add our app code to python path:
ENV PYTHONPATH="/app/src"

# Running as non-root user:
USER web

CMD ["python"]
