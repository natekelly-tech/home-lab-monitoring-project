# LabWatch — Auxcon Technologies

A full-stack home lab monitoring system that checks the status of network services and infrastructure via HTTP checks. Exposes data through a REST API, a web dashboard, and an Android mobile app.

---

## Live Deployment

| Resource | URL |
|---|---|
| Public API | https://api.auxcon.dev/status |
| Web Dashboard | https://api.auxcon.dev/dashboard |
| DockerHub | hub.docker.com/r/auxcon/labwatch-api |

The API runs 24/7 on AWS EC2 (us-west-1) behind a Cloudflare Tunnel. No home network infrastructure is exposed.

---

## Architecture

```
Internet → Cloudflare (TLS) → Cloudflare Tunnel → EC2 (AWS us-west-1)
                                                        └── Docker (Gunicorn + Flask)
```

The application runs as a non-root Docker container managed by Docker Compose. Cloudflare Tunnel handles all inbound TLS termination — no ports are directly exposed to the internet except 22 (SSH), 80, and 443, enforced by UFW and AWS Security Groups.

---

## Repository Structure

```
home-lab-monitoring-project/
backend/
  app/
    __init__.py
    main.py          # Flask routes + JSON logging
    checker.py       # HTTP check logic
    templates/
      dashboard.html # Web dashboard (military aesthetic)
  config.py          # Monitored services list
  requirements.txt   # Pinned dependencies
  Dockerfile         # Multi-stage, python:3.12-slim, non-root
  docker-compose.yml
  gunicorn.conf.py
.github/
  workflows/
    docker-build.yml # CI/CD — builds on push to main, pushes to DockerHub
diagrams/
docs/devlogs/
CHANGELOG.md
README.md
SECURITY.md
```

---

## Services Monitored

| Name | Type | Target |
|---|---|---|
| Google | HTTP | https://www.google.com |
| Cloudflare DNS | HTTP | https://1.1.1.1 |
| LabWatch API | HTTP | http://localhost:8080 |
| auxcon.dev | HTTP | https://api.auxcon.dev |

---

## API Endpoints

| Endpoint | Description |
|---|---|
| GET / | Health check — returns version info |
| GET /status | All services JSON |
| GET /status/\<name\> | Single service by name |
| GET /dashboard | Web dashboard (HTML) |

---

## Infrastructure

| Component | Details |
|---|---|
| Cloud provider | AWS EC2 us-west-1 |
| OS | Ubuntu 24.04 LTS |
| Container runtime | Docker 29.4.1 |
| WSGI server | Gunicorn 23.0.0 — 3 workers |
| Base image | python:3.12-slim |
| Container user | appuser uid 1001 (non-root) |
| Tunnel | cloudflared v2026.3.0 (systemd service) |
| Firewall | UFW + AWS Security Groups |
| Intrusion prevention | fail2ban (SSH, 5 retries / 1h ban) |
| Auto-updates | unattended-upgrades (enabled) |

---

## CI/CD

Push to `main` triggers GitHub Actions which builds a multi-platform image (`linux/amd64`, `linux/arm64`) and pushes to DockerHub as `auxcon/labwatch-api:0.3.0` and `auxcon/labwatch-api:latest`.

EC2 deployment uses the `latest` tag. To deploy a new release on EC2:

```bash
cd ~/lab
docker compose pull
docker compose up -d
```

---

## Mobile App

React Native / Expo app connecting to `https://api.auxcon.dev`. APK built and functional. Repo: github.com/natekelly-tech/homelab-app

---

## Key Design Decisions

**python:3.12-slim over alpine** — Alpine musl libc breaks C-extension Python packages silently. Slim is minimal Debian with predictable behaviour.

**Non-root container user** — If a vulnerability achieves code execution, uid 1001 limits blast radius versus running as root.

**Cloudflare Tunnel over direct exposure** — Handles TLS termination at the edge. No open inbound ports required beyond what AWS Security Groups permit.

**EC2 over home lab for production** — 9-hour time zone difference between developer (Germany) and instructor/peers (US West Coast) made home lab uptime incompatible with a production deployment. EC2 runs 24/7 independent of local infrastructure.

**Pinned dependency versions** — Reproducible builds. Unpinned dependencies produce images that differ between build dates.

---

## Project Phase Status

| Phase | Description | Status |
|---|---|---|
| 1 | Lab Setup & Network Architecture | Complete |
| 2 | Monitoring System (HTTP + Ping) | Complete |
| 3 | Backend REST API (Flask) | Complete |
| 4 | Mobile App Integration | Complete |
| 5 | External Access via Cloudflare Tunnel | Complete |
| 6 | Containerisation (Docker + DockerHub) | Complete |
| 6.5 | Cloud Migration to AWS EC2 | Complete |
| 6.6 | Server Hardening (UFW, fail2ban, unattended-upgrades) | Complete |
| 7 | Kubernetes Orchestration | Next |
