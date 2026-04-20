# Security Policy — LabWatch by Auxcon Technologies

---

## Supported Versions

| Version | Supported |
|---|---|
| 0.3.0 (current) | Yes |
| 0.2.0 | No |
| 0.1.0 | No |

---

## Infrastructure Security Posture (as of 2026-04-20)

### Network Layer — AWS Security Groups

Inbound rules enforced at the AWS network level before traffic reaches the instance:

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 22 | TCP | Anywhere | SSH access |
| 80 | TCP | Anywhere | HTTP |
| 443 | TCP | Anywhere | HTTPS |

All other inbound traffic is denied by default at the AWS Security Group level.

### OS Layer — UFW Firewall

A second firewall layer at the OS level on EC2:

| Rule | Port | Action |
|---|---|---|
| Incoming default | All | DENY |
| Outgoing default | All | ALLOW |
| SSH | 22 | ALLOW |
| HTTP | 80 | ALLOW |
| HTTPS | 443 | ALLOW |
| API direct access | 8080 | DENY |

Port 8080 is explicitly denied externally. The API is only reachable via Cloudflare Tunnel internally.

### Intrusion Prevention — fail2ban

fail2ban monitors SSH login attempts and auto-bans offending IPs.

| Setting | Value |
|---|---|
| Max retries | 5 |
| Find window | 10 minutes |
| Ban duration | 1 hour |
| Jail | sshd |

### Automatic Updates — unattended-upgrades

Security patches are applied automatically via unattended-upgrades. No manual intervention required for OS-level CVE remediation.

### Access Control

- SSH password authentication is disabled
- Root login via SSH is disabled
- Only ed25519 key authentication is accepted
- Docker container runs as non-root appuser (uid 1001)

### Public Exposure

The API is not directly exposed to the internet. All public traffic routes through Cloudflare Tunnel:

```
Internet → Cloudflare Edge (TLS 1.3) → Cloudflare Tunnel → localhost:8080
```

No inbound port is opened for the API itself. Cloudflare handles TLS termination.

---

## Container Security Posture

### Trivy Scan Results (2026-04-19 — post-fix)

Full scan results: `security-reports/trivy-2026-04-19-post-fix.txt`

| Category | Count | Status |
|---|---|---|
| CRITICAL | 0 | Clean |
| HIGH — remediated | 1 | OpenSSL CVE-2026-28390 — fixed via apt-get upgrade in Dockerfile |
| HIGH — upstream blocked | 6 | ncurses (4 pkgs), systemd (2 pkgs) — no fix available from Debian |
| Python deps — remediated | 3 | requests x2 (bumped to 2.33.0), pip x1 (upgraded in Dockerfile) |
| MEDIUM — upstream blocked | 26 | glibc, util-linux, xz, zlib, tar, systemd — no fix available |
| Secrets found | 0 | Clean |

### Upstream-Blocked CVE Risk Assessment

**systemd (2 HIGH)** — libsystemd0 is a library on disk only. systemd is not running as PID 1 in the container. The CVEs require systemd to be executing to be exploitable. Risk: negligible.

**ncurses (4 HIGH)** — LabWatch is a headless HTTP API. It never invokes terminal UI rendering. The ncurses library is never called at runtime. Risk: negligible.

**MEDIUM findings** — glibc, util-linux, xz, zlib, tar, systemd. All upstream-blocked with no available fixes. Monitored for upstream resolution.

---

## Reporting a Vulnerability

This is a university course project. If you identify a vulnerability during authorised red-team testing, document your findings and report them through the course channel. Do not attempt to access, modify, or exfiltrate any data beyond confirming the existence of a vulnerability.
