import requests
import subprocess

TIMEOUT_SECONDS = 5


def check_http(name, url):
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response_time_ms = round(response.elapsed.total_seconds() * 1000)
        return {
            "name": name,
            "type": "http",
            "target": url,
            "status": "up",
            "response_time_ms": response_time_ms,
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException:
        return {
            "name": name,
            "type": "http",
            "target": url,
            "status": "down",
            "response_time_ms": None,
            "status_code": None
        }


def check_ping(name, host):
    try:
        result = subprocess.run(
            ["/usr/bin/ping", "-c", "1", "-W", "3", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT_SECONDS
        )
        is_up = result.returncode == 0
        return {
            "name": name,
            "type": "ping",
            "target": host,
            "status": "up" if is_up else "down",
            "response_time_ms": None,
            "status_code": None
        }
    except Exception:
        return {
            "name": name,
            "type": "ping",
            "target": host,
            "status": "down",
            "response_time_ms": None,
            "status_code": None
        }


def check_service(service):
    if service.get("type") == "ping":
        return check_ping(service["name"], service["host"])
    else:
        return check_http(service["name"], service["url"])


def check_all_services(services):
    return [check_service(s) for s in services]
