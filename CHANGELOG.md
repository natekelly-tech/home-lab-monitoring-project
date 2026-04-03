# Changelog

All notable changes to the Enterprise-Style Home Lab Monitoring Project will be documented in this file.

---

## v1.0 – Baseline Architecture Defined

* Finalized core network topology:

  * ISP → Home Router / Gateway → Cisco Switch (SW1)
* Established Layer 2 switching model with planned VLAN segmentation
* Defined network segmentation strategy:

  * VLAN 10 – Management network (Main PC / Command Station)
  * VLAN 20 – Lab network (Lab Server and virtualized systems)
* Introduced dedicated Lab Server (VM Host) to separate infrastructure from management systems
* Defined internal virtualization layer using a virtual switch for VM-to-VM communication
* Structured the Virtualized Lab Environment with clearly defined roles:

  * Web Server VM (HTTP service)
  * Client VM (user simulation)
  * Monitoring Backend VM (API backend)
* Implemented management communication path between Main PC and Lab Server (SSH / API)
* Integrated mobile device (monitoring app) over WiFi (WLAN) to simulate real-world user access
* Defined API-based monitoring flow:

  * Mobile device → Router → Switch → Lab Server → Monitoring Backend VM
* Improved diagram clarity, labeling, and separation of physical vs logical connections

This version represents the baseline architecture that future implementation and development will be built on.

---

## v0.3 – Mobile Integration and Full Architecture Flow

* Added mobile device (monitoring app) connected via WiFi (WLAN)
* Introduced API communication path from mobile device to lab backend (HTTPS)
* Clarified end-to-end system flow: client → API → lab environment
* Improved diagram layout for readability and separation of roles
* Refined labeling for management traffic and API access paths

---

## v0.2 – Network Structure and Virtualization Layer

* Introduced Cisco switch (SW1) as central network device
* Defined network segmentation using VLAN concepts:

  * VLAN 10 (Management)
  * VLAN 20 (Lab Network)
* Added dedicated lab server (VM host) to separate infrastructure from management system
* Introduced virtual switch concept for internal VM networking
* Grouped virtual machines into a structured "Virtualized Lab Environment"
* Defined VM roles:

  * Web Server VM (HTTP service)
  * Client VM (user simulation)
  * Monitoring Backend VM (API backend)

---

## v0.1 – Initial Topology Concept

* Created initial high-level network diagram
* Defined core components:

  * ISP connection
  * Home router / gateway
  * Main PC (management system)
  * Lab server concept
* Established basic communication flow between systems
* Outlined intent to simulate an enterprise-style home lab environment
