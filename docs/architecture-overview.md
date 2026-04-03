# Architecture Overview

This document explains the design and structure of the home lab monitoring system.

---

## Network Design

The lab is structured to simulate an enterprise-style environment.

### Core Components
- ISP connection
- Home router / gateway
- Cisco switch (SW1)
- Lab server (VM host)
- Management workstation

---

## Network Segmentation

The network is divided using VLANs:

- VLAN 10 – Management Network  
  Used for administration and control

- VLAN 20 – Lab Network  
  Used for virtual machines and services

---

## Virtualization Layer

The lab server hosts multiple virtual machines connected through a virtual switch.

### VM Roles
- Web Server VM  
  Hosts HTTP services

- Client VM  
  Simulates user traffic

- Monitoring Backend VM  
  Runs monitoring logic and API

---

## Monitoring Flow

1. Monitoring service runs on backend VM
2. Backend checks services across lab
3. API exposes system health data
4. Mobile device retrieves data via API

---

## Design Goals

- Isolation between management and lab systems
- Realistic enterprise structure
- Scalable architecture for future expansion
