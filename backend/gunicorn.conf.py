# gunicorn.conf.py — LabWatch API
# Gunicorn replaces Flask's built-in dev server, which is single-threaded,
# exposes a live debugger over the network, and does not handle SIGTERM
# correctly for graceful container shutdown.

import os

bind = "0.0.0.0:8080"

# Formula: (2 × CPU cores) + 1. VM has 1–2 vCPUs, so 3 is correct.
# Scale-out at load happens via Kubernetes HPA across pods, not more workers here.
workers = int(os.environ.get("GUNICORN_WORKERS", "3"))

worker_class = "sync"

# /status runs all checks synchronously. ProtonVPN routing can push a single
# check to ~40s, so timeout must exceed the worst-case total check time.
timeout = 120

# Logs to stdout/stderr so Docker captures them with `docker logs`.
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()

# Structured access log — one JSON object per request, aggregator-ready.
access_log_format = '{"remote_ip":"%(h)s","method":"%(m)s","path":"%(U)s","status":%(s)s,"duration_us":%(D)s,"bytes":%(b)s}'

proc_name = "labwatch-api"
