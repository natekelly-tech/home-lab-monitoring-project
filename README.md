# Enterprise-Style Home Lab Monitoring Project

## Overview

This project is a personal home lab designed to simulate a small enterprise network environment. The goal is to build a realistic setup that includes network segmentation, virtualized systems, and a lightweight monitoring solution with a mobile interface.

The project is being developed in phases, starting with a foundational lab and expanding into backend services and application-level monitoring.

---

## Architecture

The lab environment includes:

* ISP → Router → Cisco Switch topology
* Dedicated lab server hosting virtual machines
* Segmented network design (management and lab networks)
* Virtualized lab environment including:

  * Web server
  * Client system
  * Monitoring backend

A mobile device will be used to access monitoring data through a custom API over WiFi.

See `/diagrams` for topology diagrams.

---

## Project Components

### 1. Lab Environment

* Cisco switch-based network
* VLAN segmentation (planned/implemented)
* Virtual machines running services and test systems

### 2. Backend Monitoring

* Python-based backend (Flask or FastAPI)
* Performs basic checks (ping, service availability)
* Exposes data through a simple API

### 3. Mobile App (Planned)

* Mobile interface to view system status
* Connects to backend API
* Displays device and service health

---

## Goals

* Build a realistic and expandable home lab
* Reinforce networking concepts (CCNA-level)
* Learn backend development and API design
* Gain exposure to mobile application development
* Create a portfolio-ready project

---

## Project Status

Currently in early development:

* Architecture design complete
* Initial lab setup in progress

---

## Changelog

See `CHANGELOG.md` for version history and updates.
