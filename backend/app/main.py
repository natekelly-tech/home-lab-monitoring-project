from flask import Flask, jsonify, render_template
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import SERVICES
from app.checker import check_service

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "Homelab Monitor API is running"})

@app.route("/status")
def status_all():
    results = [check_service(s) for s in SERVICES]
    return jsonify(results)

@app.route("/status/<name>")
def status_one(name):
    for s in SERVICES:
        if s["name"].lower() == name.lower():
            return jsonify(check_service(s))
    return jsonify({"error": "Service not found"}), 404

@app.route("/dashboard")
def dashboard():
    results = [check_service(s) for s in SERVICES]
    return render_template("dashboard.html", services=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
