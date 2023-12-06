FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1

COPY Pipfile Pipfile.lock .

RUN apt-get update && \
    apt-get install -y --no-install-recommends vim libpq-dev build-essential && \
    pip install -U pip && pip install pipenv && \
    CI=1 PIPENV_NOSPIN=1 pipenv install --system --deploy && \
    apt-get purge -y --auto-remove build-essential && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY app/ /app
