# Mobile App Overview

## Purpose

The mobile application is a lightweight network monitoring tool designed to interact with the home lab environment.

Its primary purpose is to provide basic visibility into system and network status from a mobile device.

---

## Current Scope (Phase 1–2)

The mobile app is intentionally limited in scope to avoid overengineering.

### Core Features
- View system status (online/offline)
- Check availability of lab services (e.g., HTTP server)
- Display basic network health information
- Send simple requests to the backend API

---

## How It Fits Into the System

The mobile app does not directly monitor systems.

Instead, it acts as a client to the backend:

### Flow
1. Mobile app sends request to API
2. API queries monitoring backend
3. Backend checks lab services
4. Results returned to mobile app

---

## Technology Considerations (Planned)

This project has not yet selected a final mobile framework.

Possible options:
- React Native
- Flutter
- Simple web-based mobile interface

Final decision will depend on:
- project complexity
- time constraints
- backend integration requirements

---

## Future Enhancements

- Push notifications for system alerts
- Authentication (user login)
- Historical data visualization
- Dashboard-style UI

---

## Design Philosophy

- Keep it simple
- Focus on functionality over appearance
- Prioritize backend integration first
- Treat mobile app as a client, not the core system
