# Home Lab Monitoring Project

A full-stack enterprise-style home lab monitoring system built on a physical network with virtual machines, a Python REST API, and a native Android mobile app.

---

## Overview

This project simulates an enterprise monitoring environment from the ground up — physical network infrastructure, Linux server deployment, a custom REST API, and a mobile app that displays live service status in real time.

Built as part of a university BETA project. All components are self-hosted and self-managed.

---

## Architecture

```
Android App (LabWatch)
        |
   auxcon.dev (Cloudflare Tunnel)
        |
Ubuntu Server VM (192.168.2.137)
        |
   Flask REST API (Port 8080)
        |
   Monitoring Engine
   (HTTP checks + Ping)
        |
 [Google] [Cloudflare DNS] [Router] [Main PC] [Lab PC] [Ubuntu Server]
```

### Network Infrastructure

| Device | IP | Role |
|--------|-----|------|
| Speedport Smart 4 | 192.168.2.1 | Home router (Deutsche Telekom) |
| Main PC (Windows) | 192.168.2.100 | Development machine |
| Lab PC (Windows) | 192.168.2.123 | VM host machine |
| Ubuntu Server VM | 192.168.2.137 | Production server |

---

## Project Structure

```
home-lab-monitoring-project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Flask app and routes
│   │   ├── checker.py       # HTTP and ping check logic
│   │   └── templates/
│   │       └── dashboard.html
│   ├── config.py            # Monitored services config
│   └── requirements.txt
├── diagrams/                # Network topology diagrams
├── docs/                    # Documentation and dev logs
├── lab/                     # Lab setup notes
├── scripts/                 # Helper scripts
├── CHANGELOG.md
└── README.md
```

---

## Backend — Flask REST API

**Runtime:** Python 3 with Flask  
**Host:** Ubuntu Server VM at `192.168.2.137`  
**Process manager:** systemd (auto-starts on boot)

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/status` | All services JSON |
| GET | `/status/<name>` | Single service status |
| GET | `/dashboard` | Web dashboard |

### Services Monitored

| Service | Type | Target |
|---------|------|--------|
| Google | HTTP | https://www.google.com |
| Cloudflare DNS | HTTP | https://1.1.1.1 |
| Speedport Router | HTTP | http://192.168.2.1 |
| Main PC | Ping | 192.168.2.100 |
| Lab PC | Ping | 192.168.2.123 |
| Ubuntu Server | Ping | 127.0.0.1 |

---

## Mobile App — LabWatch

A native Android app built with React Native and Expo that displays live service status from the Flask API.

**Repository:** [github.com/natekelly-tech/homelab-app](https://github.com/natekelly-tech/homelab-app)  
**Package ID:** `com.auxcon.labwatch`  
**Built with:** React Native, Expo, EAS Build

---

## Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Lab Setup and Network Architecture | Complete |
| Phase 2 | Monitoring System (HTTP + Ping) | Complete |
| Phase 3 | Backend REST API (Flask) | Complete |
| Phase 4 | Mobile App Integration | Complete |
| Phase 5 | External Access via Cloudflare Tunnel | In Progress |
| Future | Docker, Kubernetes, Authentication, Alerts | Planned |

---

## Documentation

- [CHANGELOG.md](CHANGELOG.md) — version history
- [docs/devlogs/](docs/devlogs/) — session dev logs
- [diagrams/](diagrams/) — network topology diagrams

---

## Author

**Nathaniel Kelly**  
Auxcon Technologies  
GitHub: [github.com/natekelly-tech](https://github.com/natekelly-tech)
