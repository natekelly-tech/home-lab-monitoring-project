# Enterprise-Style Home Lab Monitoring Project

## Overview
This project is a hands-on cybersecurity and networking lab designed to simulate an enterprise environment.

The goal is to build a fully segmented home lab with monitoring capabilities, backend services, and a mobile interface.

---

## Objectives
- Build a segmented home lab network using VLANs
- Deploy and manage virtual machines on a dedicated lab server
- Develop a Python-based monitoring system
- Expose monitoring data through an API
- Integrate a mobile application for real-time monitoring

---

## Architecture

See `/diagrams` for full topology diagrams.

### Current Design Includes

- ISP → Router → Cisco Switch (SW1)
- VLAN segmentation (Management + Lab)
- Dedicated Lab Server (VM host)
- Virtualized environment with multiple VMs
- Mobile device integration via WiFi

---

## Project Structure

home-lab-monitoring-project/
├── diagrams/   # Network and architecture diagrams
├── docs/       # Planning and documentation
├── lab/        # Lab setup and configuration
├── backend/    # Future Python API/backend
└── scripts/    # Helper scripts

---

### Phase 1 – Lab Setup

| Task | Status |
|------|--------|
| Architecture defined | ✅ |
| Repo structure complete | ✅ |
| Diagrams created | ✅ |
| Lab setup | 🔄 |

---

## Roadmap
See: `docs/project-roadmap.md`

---

## Changelog
See: `CHANGELOG.md`

---

## Author
Nathaniel Kelly  
GitHub: https://github.com/natekelly-tech
