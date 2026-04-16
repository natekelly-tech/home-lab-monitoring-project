import subprocess
import requests

def check_service(service):
    if service["type"] == "http":
        try:
            response = requests.get(service["url"], timeout=10)
            return {"name": service["name"], "status": "up", "code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"name": service["name"], "status": "down", "error": str(e)}

    elif service["type"] == "ping":
        try:
            result = subprocess.run(
                ["/usr/bin/ping", "-c", "1", "-W", "3", service["host"]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            status = "up" if result.returncode == 0 else "down"
            return {"name": service["name"], "status": status}
        except Exception as e:
            return {"name": service["name"], "status": "down", "error": str(e)}

    return {"name": service["name"], "status": "unknown"}
