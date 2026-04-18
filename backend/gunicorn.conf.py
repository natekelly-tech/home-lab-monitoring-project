# gunicorn.conf.py
# Gunicorn configuration for LabWatch API
# This file is read by: gunicorn --config gunicorn.conf.py app.main:app
#
# Gunicorn is a production WSGI server. It replaces Flask's built-in
# development server (app.run()), which is:
#   - Single-threaded (one request at a time)
#   - Not designed for concurrent load
#   - Exposes a live debugger over the network when debug=True
#   - Does not handle OS signals (SIGTERM) correctly for clean shutdown
#
# Gunicorn spawns multiple worker processes that each handle requests
# independently, and it handles signals and restarts properly.

import os

# ── Binding ─────────────────────────────────────────────────────────────────
# Listen on all interfaces (0.0.0.0) so Docker can route traffic into us.
# Port 8080 to match the existing Flask setup.
bind = "0.0.0.0:8080"

# ── Workers ──────────────────────────────────────────────────────────────────
# Number of worker processes. Industry formula: (2 × CPU cores) + 1
# Your VM likely has 1–2 vCPUs, so 3 workers is the right starting point.
# Each worker is a full Python process that handles one request at a time.
# 3 workers = 3 simultaneous requests before any queueing starts.
#
# For a home lab monitor: 3 is more than enough.
# For "hundreds of thousands of users": you'd scale this via Kubernetes
# HorizontalPodAutoscaler across many pods, not by adding workers here.
workers = int(os.environ.get("GUNICORN_WORKERS", "3"))

# ── Worker class ─────────────────────────────────────────────────────────────
# "sync" = the default. One request per worker at a time.
# "gthread" = threaded workers (handles concurrent I/O better).
# For a monitoring API that does network I/O (HTTP checks, pings), gthread
# is actually a better fit. We keep sync for simplicity — defensible choice.
worker_class = "sync"

# ── Timeouts ─────────────────────────────────────────────────────────────────
# How long gunicorn waits for a worker to respond before killing it.
# Your /status endpoint runs all checks synchronously — if you're monitoring
# 6 services and the slowest takes ~40s (ProtonVPN), this needs to be higher
# than that or gunicorn will kill the worker mid-request.
timeout = 120

# ── Logging ──────────────────────────────────────────────────────────────────
# "-" means stdout/stderr. Docker captures these streams.
# This is how your logs end up in `docker logs labwatch-api`.
# A log aggregator (Loki, CloudWatch) reads Docker's captured streams.
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()

# Access log format — structured so it's parseable by log aggregators.
# %(h)s = remote IP, %(m)s = HTTP method, %(U)s = URL path,
# %(s)s = status code, %(D)s = response time in microseconds
access_log_format = '{"remote_ip":"%(h)s","method":"%(m)s","path":"%(U)s","status":%(s)s,"duration_us":%(D)s,"bytes":%(b)s}'

# ── Process naming ────────────────────────────────────────────────────────────
# Makes the process identifiable in `ps` and container monitoring tools.
proc_name = "labwatch-api"
