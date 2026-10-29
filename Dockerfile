# The public play server (python -m clocktower play): tables, games and spend in /data (mount a volume there).
# Build: docker build -t clocktower-play .   Run: see docs/hosting.md.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    PLAY_DATA_DIR=/data

WORKDIR /app
COPY pyproject.toml ./
COPY clocktower ./clocktower
RUN pip install . && useradd --create-home --uid 10001 clocktower && mkdir -p /data && chown clocktower /data

USER clocktower
VOLUME ["/data"]
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/healthz', timeout=4)"
CMD ["sh", "-c", "exec python -m clocktower play --host 0.0.0.0 --port ${PORT}"]
