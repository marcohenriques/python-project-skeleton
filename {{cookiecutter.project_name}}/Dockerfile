# Settings --------------------------------------------------------------------
ARG PYTHON_VERSION={{ cookiecutter.python_version }}
ARG BASE_IMAGE_TYPE=slim
ARG VENV_PATH="/opt/venv"

# STAGE: Compile --------------------------------------------------------------
FROM python:${PYTHON_VERSION} AS compile-image

ARG VENV_PATH

RUN apt-get update \
    && python -m venv "${VENV_PATH}"

ENV PATH="${VENV_PATH}/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

COPY requirements.txt /
RUN pip install -U pip \
    && pip install -r /requirements.txt

# STAGE: Build ----------------------------------------------------------------
FROM python:${PYTHON_VERSION}-${BASE_IMAGE_TYPE} AS build-image

ARG VENV_PATH
ARG UID=1000
ARG GID=1000
ARG APP_NAME="{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"

# get installed python packages
COPY --from=compile-image "${VENV_PATH}" "${VENV_PATH}"

WORKDIR /app

# Make sure we use the virtualenv:
ENV PATH="${VENV_PATH}/bin:$PATH" \
    PYTHONPATH="/app/src"


RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    tini=0.19.0-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Create custom user and group to run the app
    && groupadd --gid "${GID}" --system "${APP_NAME}" \
    && useradd --home-dir /app --gid "${APP_NAME}" --no-log-init --system --uid "${UID}" "${APP_NAME}" \
    && chown "${APP_NAME}":"${APP_NAME}" -R /app


# We customize how our code is loaded with the custom entrypoint:
COPY ./docker/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY src src

# STAGE: Production -----------------------------------------------------------
FROM build-image AS production

# Running as non-root user:
USER ${APP_NAME}

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]
CMD ["python"]
