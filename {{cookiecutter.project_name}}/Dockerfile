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

WORKDIR /code

# Add our app code to python path:
ENV PYTHONPATH="/code/src"

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    procps \
    build-essential \
    gcc \
    tini \
    # Create custom user and group to run the app as:
    && groupadd -g "${GID}" -r app \
    && useradd -d /code -g app -l -r -u "${UID}" app \
    && chown app:app -R /code

COPY requirements.txt /
RUN pip install -U pip \
    && pip install -r /requirements.txt

# We customize how our code is loaded with the custom entrypoint:
COPY ./docker/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]


# # 'production' stage uses the clean 'python-base' stage and copyies
# # in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production

COPY . .

# Running as non-root user:
USER app

CMD ["python"]


# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /code
FROM python-base as development

COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt

# Instead of copying the whole project, we could mount a volume to current directory:
# COPY . .

# Running as non-root user:
USER app

CMD ["python"]
