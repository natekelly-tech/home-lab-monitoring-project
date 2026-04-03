# Changelog

All notable changes to this project will be documented in this file.

This project follows a structured, versioned approach to track architecture, lab development, and software implementation.

---

## Current Phase: Phase 1 – Setup

### Completed
- Initial repository created
- Repository structure established:
  - `docs/`
  - `diagrams/`
  - `lab/`
  - `backend/`
  - `scripts/`
- Added starter `README.md` files to all directories
- Created `CHANGELOG.md`
- Created `project-roadmap.md`
- Created `lab-plan.md`
- Added initial network diagrams:
  - `Topology v1.0.drawio`
  - `Topology v1.0.png`
- Defined baseline architecture and system design

### In Progress
- Lab server build
- VM setup and configuration

### Planned
- Python monitoring script
- Backend API development
- Mobile application integration

---

## [v1.0] – Baseline Architecture Defined

### Added
- Finalized core network topology:
  - ISP → Home Router / Gateway → Cisco Switch (SW1)
- Defined Layer 2 switching model
- Designed VLAN segmentation strategy:
  - VLAN 10 – Management network
  - VLAN 20 – Lab network
- Introduced dedicated Lab Server (VM Host)
- Defined internal virtualization layer (virtual switch)
- Structured virtualized lab environment:
  - Web Server VM (HTTP service)
  - Client VM (user simulation)
  - Monitoring Backend VM (API backend)
- Established management communication path (SSH / API)
- Added mobile device integration over WLAN
- Defined API-based monitoring flow:
  - Mobile → Router → Switch → Lab Server → Backend VM
- Created and uploaded architecture diagrams (v1.0)
- Improved diagram clarity and labeling

---

## [v0.3] – Mobile Integration and Full Architecture Flow

### Added
- Mobile device (monitoring app) connected via WiFi
- API communication path using HTTPS
- End-to-end system flow:
  - Client → API → Lab Environment

### Changed
- Improved diagram layout and readability
- Refined labeling for:
  - Management traffic
  - API access paths

---

## [v0.2] – Network Structure and Virtualization Layer

### Added
- Cisco switch (SW1) as central network device
- VLAN segmentation design:
  - VLAN 10 – Management
  - VLAN 20 – Lab Network
- Dedicated Lab Server (VM host)
- Virtual switch for internal VM networking
- Structured "Virtualized Lab Environment"

### Defined VM Roles
- Web Server VM
- Client VM
- Monitoring Backend VM

---

## [v0.1] – Initial Topology Concept

### Added
- Initial high-level network diagram
- Core components defined:
  - ISP connection
  - Home router / gateway
  - Main PC (management system)
  - Lab server concept
- Basic communication flow between systems
- Defined project goal:
  - Simulate an enterprise-style home lab environment

---

## Repository Setup (GitHub Initialization)

### Added
- Public GitHub repository created
- Initial commits on `main` branch
- `.gitignore` added
- Root `README.md` created and expanded
- Folder structure created via GitHub web interface
- Markdown documentation initialized across project

### Notes
- Project is currently managed directly on `main` (no branching yet)
- Workflow intentionally kept simple for early-stage development
