# Changelog

All notable changes to the Enterprise-Style Home Lab Monitoring Project will be documented in this file.

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
