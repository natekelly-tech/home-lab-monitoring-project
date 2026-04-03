# Project Roadmap

This roadmap outlines the planned phases of the Enterprise-Style Home Lab Monitoring Project.

---

## Phase 1 – Lab Setup (Current)

### Goals
- Design network architecture
- Build lab environment
- Establish virtualization layer

### Tasks
- [x] Create network topology diagram
- [x] Define VLAN segmentation
- [x] Create repository structure
- [x] Document lab plan
- [ ] Build lab server
- [ ] Deploy virtual machines

---

## Phase 2 – Monitoring System

### Goals
- Develop backend monitoring capability

### Tasks
- [ ] Create Python monitoring script
- [ ] Implement service checks (HTTP, ping, etc.)
- [ ] Log system health data
- [ ] Define API structure

---

## Phase 3 – Backend API

### Goals
- Expose monitoring data via API

### Tasks
- [ ] Build API (Flask or FastAPI)
- [ ] Create endpoints for:
  - system status
  - service health
- [ ] Test API locally

---

## Phase 4 – Mobile Integration

### Goals
- Create user interface for monitoring

### Tasks
- [ ] Design mobile app interface
- [ ] Connect to backend API
- [ ] Display real-time system data

---

## Future Enhancements

- Authentication system
- Alerting (email / push notifications)
- Dashboard UI (web-based)
- Cloud integration
