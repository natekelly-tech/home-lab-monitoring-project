# syntax=docker/dockerfile:1
# ================================================================
# Auxcon Technologies — LabWatch Monitoring API
# Production Dockerfile — multi-stage build
#
# Two stages:
#   builder  — installs dependencies (has pip, wheel, build tools)
#   runtime  — runs the app (has nothing extra; builder is discarded)
#
# The final image contains:
#   - Python 3.12 slim runtime
#   - Installed packages from requirements.txt (no pip itself)
#   - Application source code only
#   - A non-root user (appuser)
#   - No shell scripts, no secrets, no build artefacts
# ================================================================


# ──────────────────────────────────────────────────────────────
# STAGE 1: builder
# Purpose: install Python dependencies into a virtual environment.
# This entire stage is thrown away after the build — none of the
# build tooling reaches the final image.
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy requirements first, before any application code.
# Why: Docker caches each instruction as a layer on disk.
# If requirements.txt hasn't changed between builds, Docker reuses
# the cached pip install layer and skips it entirely — saving minutes
# on every rebuild. If you copied the whole app first, any code change
# would invalidate the cache and re-run pip every time.
COPY requirements.txt .

# Create a virtual environment and install dependencies into it.
# --no-cache-dir: don't save pip's download cache inside the image
# --quiet: less noise in build output
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip --quiet \
    && /opt/venv/bin/pip install --no-cache-dir --quiet -r requirements.txt


# ──────────────────────────────────────────────────────────────
# STAGE 2: runtime
# Purpose: the actual container that runs in production.
# Starts from the same base, but only receives:
#   - The compiled venv from the builder stage
#   - Application source code
# No pip. No build tools. No compiler. Smaller attack surface.
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Create a dedicated non-root user and group for the application.
#
# Why non-root? Containers run as root by default. If your app has a
# vulnerability and an attacker achieves code execution, they run as
# root inside the container — which on host-networked containers means
# root on the host too. Running as an unprivileged user limits blast
# radius significantly. This is a basic container hardening requirement.
#
# --system:        creates a system account (no home dir, no password)
# --gid/--uid 1001: explicit IDs so they're consistent and auditable
# --no-create-home: no /home/appuser directory needed
RUN groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid appgroup --no-create-home appuser

# Set the working directory. All subsequent paths are relative to this.
WORKDIR /app

# Copy the fully-installed virtual environment from the builder stage.
# We get all the installed packages without pip, wheel, or any build
# tooling that was used to install them.
COPY --from=builder /opt/venv /opt/venv

# Copy application files.
# config.py before app/ — config changes less often than app code,
# so this layer ordering maximises cache reuse.
COPY config.py .
COPY gunicorn.conf.py .
COPY app/ ./app/

# Transfer ownership of everything under /app to our non-root user.
# Must be done as root (before the USER switch) because chown requires
# privilege. After this line, appuser owns the files and can read them,
# but no one is running as root anymore.
RUN chown -R appuser:appgroup /app

# Switch to non-root user for all subsequent RUN, CMD, ENTRYPOINT.
# Any vulnerability exploited after this point runs as uid 1001.
USER appuser

# Environment variables baked into the image.
#
# PATH:                   put venv bin first so 'gunicorn', 'python', etc.
#                         resolve to our venv without full paths
# PYTHONUNBUFFERED=1:     force Python to flush stdout/stderr immediately
#                         without this, logs may not appear in Docker until
#                         a buffer fills — makes live log tailing unreliable
# PYTHONDONTWRITEBYTECODE=1: don't write .pyc bytecode files to disk
#                            cleaner image, slightly faster startup
# PYTHONPATH=/app:        tells Python to look in /app for modules
#                         this is why 'from config import SERVICES' works
#                         without the sys.path hack in main.py
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Document that the container listens on 8080.
# EXPOSE is metadata only — it does NOT open the port.
# The actual port mapping happens with -p at runtime or ports: in compose.
EXPOSE 8080

# Health check: hit the / endpoint periodically.
# Docker marks the container unhealthy if this fails --retries times.
# Kubernetes liveness probes will do the same job in K8s — this is the
# container-native equivalent of systemd's Restart=always.
#
# We use Python's built-in urllib (no extra tools to install).
# --start-period=15s: give gunicorn time to start before first check.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c \
        "import urllib.request; urllib.request.urlopen('http://localhost:8080/')" \
        || exit 1

# Start command: gunicorn reads its config from gunicorn.conf.py
# and then loads the Flask app object from app/main.py.
#
# "app.main:app" means:
#   app.main  → the Python module at app/main.py
#   :app      → the Flask object named 'app' inside that module
#
# We use the JSON list form (exec form) not the string form (shell form).
# Shell form runs via /bin/sh -c which adds an extra process and means
# signals (SIGTERM from docker stop) don't reach gunicorn — graceful
# shutdown breaks. Exec form sends signals directly to gunicorn.
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app.main:app"]
