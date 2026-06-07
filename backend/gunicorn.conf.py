# gunicorn.conf.py — LabWatch API
# Gunicorn replaces Flask's built-in dev server, which is single-threaded,
# exposes a live debugger over the network, and does not handle SIGTERM
# correctly for graceful container shutdown.

import os
import sys

# Server Socket
bind = "0.0.0.0:8080"

# Scale-out at load happens via Kubernetes HPA across pods, not more workers here.
workers = int(os.environ.get("GUNICORN_WORKERS", "2"))

worker_class = "sync"

# /status runs all checks synchronously. ProtonVPN routing can push a single
# check to ~40s, so timeout must exceed the worst-case total check time.
timeout = 120

# Logs to stdout/stderr so Docker captures them with `docker logs`.
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()

proc_name = "labwatch-api"

# JSON Log Configuration
# Replaces the fragile access_log_format string with a robust dictionary router.
# This forces Gunicorn to pass its access and error logs through the same
# python-json-logger formatter your application code uses, ensuring safe serialization.
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_access": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_access",
            "stream": sys.stdout
        }
    },
    "loggers": {
        "gunicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "gunicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        }
    }
}
