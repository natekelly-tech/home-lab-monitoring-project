# syntax=docker/dockerfile:1
# Auxcon Technologies — LabWatch API
# Multi-stage build: builder installs deps, runtime runs the app.
# The builder stage is discarded — pip and build tools never reach production.

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy requirements before app code so Docker's layer cache skips
# re-running pip install on rebuilds where only app code changed.
COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip --quiet \
    && /opt/venv/bin/pip install --no-cache-dir --quiet -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
# python:3.12-slim chosen over alpine (musl libc breaks some Python wheels)
# and distroless (too restrictive for current debugging workflow).
FROM python:3.12-slim AS runtime

# Non-root user: limits blast radius if a vulnerability achieves code execution.
RUN groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# iputils-ping: required for ICMP checks. libcap2-bin + setcap grants
# cap_net_raw to the ping binary only — minimum necessary privilege,
# not --privileged or a broad capability grant.
RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping libcap2-bin \
    && setcap cap_net_raw+ep /usr/bin/ping \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY config.py .
COPY gunicorn.conf.py .
COPY app/ ./app/

RUN chown -R appuser:appgroup /app

USER appuser

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c \
        "import urllib.request; urllib.request.urlopen('http://localhost:8080/')" \
        || exit 1

# Exec form (JSON array) used so Docker sends SIGTERM directly to gunicorn
# rather than to a shell wrapper — required for graceful shutdown.
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app.main:app"]
