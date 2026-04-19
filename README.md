# LabWatch — Home Lab Monitoring System

**Auxcon Technologies** | [auxcon.dev](https://auxcon.dev) | [api.auxcon.dev/status](https://api.auxcon.dev/status)

A full-stack, enterprise-style home lab monitoring system built from physical network infrastructure up. Monitors network devices and internet connectivity via HTTP checks and ICMP ping, exposes live data through a REST API, and displays status on a native Android app and web dashboard.

---

## Live Deployment

| Component | URL |
|-----------|-----|
| API Status | https://api.auxcon.dev/status |
| API Health | https://api.auxcon.dev/ |
| Web Dashboard | https://api.auxcon.dev/dashboard |
| Docker Image | https://hub.docker.com/r/auxcon/labwatch-api |

---

## Quick Start (Docker)

Pull and run the published image in one command:

```bash
docker pull auxcon/labwatch-api:0.2.0

docker run -d \
  --name labwatch-api \
  --network=host \
  --cap-add=NET_RAW \
  --restart=unless-stopped \
  auxcon/labwatch-api:0.2.0
```

The API will be available at `http://localhost:8080`.

> `--network=host` is required for ICMP ping checks to reach LAN devices.
> `--cap-add=NET_RAW` grants the minimum Linux capability needed for raw socket access.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check — returns version info |
| GET | `/status` | All services — JSON summary with up/down counts |
| GET | `/status/<name>` | Single service by name |
| GET | `/dashboard` | Web dashboard (HTML) |

### Example response — `/status`

```json
{
  "total": 4,
  "up": 4,
  "down": 0,
  "results": [
    {
      "name": "Google",
      "type": "http",
      "target": "https://www.google.com",
      "status": "up",
      "response_time_ms": 310,
      "status_code": 200
    },
    {
      "name": "Lab PC",
      "type": "ping",
      "target": "[LAN-HOST]",
      "status": "up",
      "response_time_ms": null,
      "status_code": null
    }
  ]
}
```

---

## Architecture

```
Architecture
Internet (Deutsche Telekom)
        |
  [HOME-ROUTER] — Speedport Smart 4
        |
  [CORE-SWITCH] — Cisco Catalyst 1200-8T-D
  ├── [DEV-MACHINE] — Windows / primary development
  └── [LAB-PC] — Windows / VirtualBox host
                    └── [PROD-SERVER] — Ubuntu Server VM
                              └── LabWatch API — Docker container :8080
                                        |
                              Cloudflare Tunnel
                                        |
                              api.auxcon.dev (public)
                                        |
                              LabWatch Android App
```

---

## Project Structure

```
home-lab-monitoring-project/
├── backend/
│   ├── app/
│   │   ├── main.py           # Flask routes
│   │   ├── checker.py        # HTTP and ping check logic
│   │   ├── __init__.py
│   │   └── templates/
│   │       └── dashboard.html
│   ├── config.py             # Monitored services list
│   ├── requirements.txt      # Pinned Python dependencies
│   ├── Dockerfile            # Multi-stage production build
│   ├── docker-compose.yml    # Local development compose
│   ├── gunicorn.conf.py      # Production WSGI configuration
│   └── .dockerignore
├── diagrams/                 # Network topology diagrams
├── docs/
│   └── devlogs/              # Session-by-session engineering log
├── lab/
├── scripts/
├── CHANGELOG.md
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Web framework | Flask 3.1.0 |
| WSGI server | Gunicorn 23.0.0 |
| Containerisation | Docker (multi-stage, python:3.12-slim) |
| Orchestration | Docker Compose / Kubernetes (Phase 7 planned) |
| CI/CD         | GitHub Actions — auto-build and push to DockerHub on push to main |
| External access | Cloudflare Tunnel |
| Mobile app | React Native / Expo (Android) |
| Network | Cisco Catalyst 1200, Deutsche Telekom ISP |
| OS | Ubuntu Server 24.04 LTS (VM) |

---

## Mobile App

**LabWatch** is a native Android app that consumes this API and displays live service status.

- Package: `com.auxcon.labwatch`
- Repo: [github.com/natekelly-tech/homelab-app](https://github.com/natekelly-tech/homelab-app)
- Connects to `https://api.auxcon.dev`
- Auto-refreshes every 30 seconds

---

## Development Setup

### Run locally without Docker

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

### Run with Docker Compose

```bash
cd backend
docker compose up --build
```

---

## Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Lab Setup & Network Architecture | Complete |
| Phase 2 | Monitoring System (HTTP + Ping) | Complete |
| Phase 3 | Backend REST API (Flask) | Complete |
| Phase 4 | Mobile App Integration (Android) | Complete |
| Phase 5 | External Access via Cloudflare Tunnel | Complete |
| Phase 6 | Containerisation (Docker + DockerHub) | Complete |
| Phase 7 | Kubernetes Orchestration               | Planned  |
| CI/CD   | GitHub Actions Docker workflow         | Complete |
| Future  | VLANs, Auth, Alerting                  | Planned  |

---

## Author

Nathaniel Kelly
GitHub: [natekelly-tech](https://github.com/natekelly-tech)
Company: AUXCON Technologies  *"Auxiliary Connection"*
