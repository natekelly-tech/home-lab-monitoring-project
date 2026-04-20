# Changelog — LabWatch by Auxcon Technologies

All notable changes to this project are documented here.

---

## [0.3.0] — 2026-04-20

### Added
- AWS EC2 deployment (us-west-1) — LabWatch now runs 24/7 in the cloud independent of home infrastructure
- SSH key-based access to EC2 from Windows development machine (ed25519)
- Cloudflare Tunnel migrated from home Ubuntu VM to EC2 — `api.auxcon.dev` now resolves to EC2
- cloudflared running as systemd service on EC2 — survives reboots automatically
- UFW firewall configured on EC2: allow 22/80/443, deny 8080, default deny incoming
- fail2ban installed and configured — SSH brute force protection (5 retries / 10 min window / 1h ban)
- Unattended upgrades confirmed active on EC2 — automatic security patches

### Changed
- Monitored services in `config.py` updated — removed home lab devices (Lab PC, Ubuntu VM), added LabWatch API self-check and auxcon.dev external check
- `docker-compose.yml` on EC2 switched from pinned `0.2.0` tag to `latest` for automatic update pickup
- GitHub Actions workflow bumped image tag to `0.3.0`
- Home VM cloudflared service disabled — EC2 is now the sole tunnel connector

### Removed
- Home lab dependency from production deployment — no home network infrastructure required for the live API

---

## [0.2.0] — 2026-04-19

### Added
- GitHub Actions CI/CD workflow — push to main auto-builds and pushes multi-platform image to DockerHub
- Multi-platform Docker build: linux/amd64 and linux/arm64 via buildx
- Trivy vulnerability scan — results committed to security-reports/
- SECURITY.md — full CVE triage and risk assessment
- Node.js action versions updated to Node.js 24 compatible

### Changed
- README internal IPs replaced with role labels (OPSEC)
- requests bumped to 2.33.0 (CVE remediation)
- pip upgraded in Dockerfile (CVE remediation)
- apt-get upgrade added to Dockerfile (fixed OpenSSL CVE-2026-28390)

### Security
- 0 CRITICAL findings post-fix
- 1 HIGH remediated (OpenSSL)
- 6 HIGH upstream-blocked (ncurses, systemd — negligible risk in headless container)
- 0 secrets detected

---

## [0.1.0] — 2026-04-18

### Added
- Flask REST API with Gunicorn (3 workers, timeout 120s)
- HTTP and ping monitoring via checker.py
- Web dashboard with military aesthetic (dashboard.html)
- Docker containerisation — multi-stage build, python:3.12-slim, non-root appuser uid 1001
- docker-compose.yml with host networking and unless-stopped restart policy
- Cloudflare Tunnel — `api.auxcon.dev` live
- React Native mobile app (Expo) connecting to live API
- DockerHub repository auxcon/labwatch-api — image 0.1.0 pushed manually
