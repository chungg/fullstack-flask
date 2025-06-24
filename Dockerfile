FROM python:3.12-slim

ENV UV_COMPILE_BYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.7.14 /uv /uvx /bin/
COPY pyproject.toml uv.lock .

# FIXME: update and properly follow https://docs.astral.sh/uv/guides/integration/docker/
RUN apt-get update && \
    apt-get install -y --no-install-recommends vim libpq-dev build-essential && \
    CI=1 uv sync --locked && \
    apt-get purge -y --auto-remove build-essential && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY app/ /app
