# Settings --------------------------------------------------------------------
ARG PYTHON_VERSION={{ cookiecutter.python_version }}
ARG BASE_IMAGE_TYPE=slim

# STAGE: Compile --------------------------------------------------------------
FROM python:${PYTHON_VERSION} AS compile-image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-group dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-group dev


# STAGE: Build ----------------------------------------------------------------
FROM python:${PYTHON_VERSION}-${BASE_IMAGE_TYPE} AS build-image

ARG UID=1000
ARG GID=1000
ARG APP_NAME="{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"

# get installed python packages
COPY --from=compile-image --chown=app:app /app /app

WORKDIR /app

# Make sure we use the virtualenv:
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    TINI_VERSION="v0.19.0"

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
COPY ./docker/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /tini \
    && chmod +x /docker-entrypoint.sh \
    # Create custom user and group to run the app
    && groupadd --gid "${GID}" --system "${APP_NAME}" \
    && useradd --home-dir /app --gid "${APP_NAME}" --no-log-init --system --uid "${UID}" "${APP_NAME}" \
    && chown "${APP_NAME}":"${APP_NAME}" -R /app


# STAGE: Production -----------------------------------------------------------
FROM build-image AS production

# Running as non-root user:
USER ${APP_NAME}

ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]
CMD ["python"]
