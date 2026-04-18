import logging
import os
import sys

from flask import Flask, jsonify, render_template
from pythonjsonlogger import jsonlogger

# ── Structured JSON logging setup ────────────────────────────────────────────
# Must happen before the Flask app is created so that Flask's own internal
# logging also uses this format.
#
# Why JSON? Plain text logs look like:
#   2026-04-18 12:00:00 INFO Status check completed
#
# JSON logs look like:
#   {"timestamp":"2026-04-18T12:00:00Z","level":"INFO","message":"Status check completed","service_count":6}
#
# The JSON version is machine-readable. A log aggregator (Loki, CloudWatch,
# Datadog) can index individual fields and let you query:
#   "show me all ERROR logs from the last hour"
#   "show me all requests where duration_ms > 5000"
# You can't do that with plain text without regex hell.

def setup_logging():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Remove any existing handlers so we don't get duplicate output
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        rename_fields={"levelname": "level", "asctime": "timestamp"}
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logging.getLogger(__name__)


log = setup_logging()

# ── Path resolution ───────────────────────────────────────────────────────────
# config.py lives one directory above app/main.py.
# When running under gunicorn with PYTHONPATH=/app set in the Docker image,
# this sys.path manipulation is redundant — Python already finds config.py.
# It is kept here so the file still works when run directly (python app/main.py)
# outside of Docker, for local development without a container.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import SERVICES
from app.checker import check_all_services, check_service

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

log.info("LabWatch API initialised", extra={"service_count": len(SERVICES)})


@app.route("/")
def index():
    return jsonify({
        "message": "Homelab Monitor is running",
        "version": "1.0"
    })


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/status")
def status():
    log.info("Running full status check")
    results = check_all_services(SERVICES)
    up_count = sum(1 for r in results if r["status"] == "up")
    log.info(
        "Status check complete",
        extra={"total": len(results), "up": up_count, "down": len(results) - up_count}
    )
    return jsonify({
        "total": len(results),
        "up": up_count,
        "down": len(results) - up_count,
        "results": results
    })


@app.route("/status/<service_name>")
def status_single(service_name):
    matched = next(
        (s for s in SERVICES if s["name"].lower() == service_name.lower()),
        None
    )
    if matched is None:
        log.warning("Service not found", extra={"requested": service_name})
        return jsonify({"error": f"Service '{service_name}' not found"}), 404

    result = check_service(matched)
    return jsonify(result)


# ── Dev server entrypoint ─────────────────────────────────────────────────────
# This block ONLY runs when you execute: python app/main.py directly.
# It is NEVER reached when gunicorn starts the app (gunicorn imports the
# 'app' object directly and manages its own server lifecycle).
#
# debug is read from the environment — never hardcoded to True.
# Hardcoded debug=True in a container image is a security vulnerability:
# it exposes an interactive Python console to anyone who triggers a 500 error.
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"Starting LabWatch in development mode (debug={debug_mode})")
    print(f"Monitoring {len(SERVICES)} services")
    print("Visit http://localhost:8080/status")
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)
