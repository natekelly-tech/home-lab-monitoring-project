import logging
import os
import sys


from flask import Flask, jsonify, render_template
from pythonjsonlogger import jsonlogger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def setup_logging():
    # JSON log format so each line is machine-readable by any log aggregator
    # (Loki, CloudWatch, Datadog). Plain text logs cannot be queried by field.
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
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

# sys.path insert retained for direct invocation (python app/main.py).
# Redundant under Docker where PYTHONPATH=/app is set in the image.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import SERVICES
from app.checker import check_all_services, check_service

app = Flask(__name__)
# TODO: Replace in-memory storage with Redis backend in Kubernetes phase
# Current limitation: limit is per-worker (3 workers = 180rpm effective limit)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)
log.info("LabWatch API initialised", extra={"service_count": len(SERVICES)})



@app.route("/")
def index():
    return jsonify({"message": "Homelab Monitor is running", "version": "1.0"})


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/status")
def status():
    log.info("Running full status check")
    results = check_all_services(SERVICES)
    up_count = sum(1 for r in results if r["status"] == "up")
    log.info("Status check complete",
             extra={"total": len(results), "up": up_count, "down": len(results) - up_count})
    return jsonify({
        "total": len(results),
        "up": up_count,
        "down": len(results) - up_count,
        "results": results
    })


@app.route("/status/<service_name>")
def status_single(service_name):
    matched = next(
        (s for s in SERVICES if s["name"].lower() == service_name.lower()), None
    )
    if matched is None:
        log.warning("Service not found", extra={"requested": service_name})
        return jsonify({"error": f"Service '{service_name}' not found"}), 404
    return jsonify(check_service(matched))


if __name__ == "__main__":
    # debug mode read from environment — never hardcoded.
    # Hardcoded debug=True exposes a live Python console over the network.
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)
