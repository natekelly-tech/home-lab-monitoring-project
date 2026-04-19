# Security Posture — LabWatch API

## Last scanned
2026-04-19 — Trivy v0.70, image auxcon/labwatch-api:dev

## Summary
- CRITICAL: 0
- HIGH (no fix available): 6
- HIGH (remediated this session): 1 — OpenSSL CVE-2026-28390
- Python deps (remediated this session): 3 — requests x2, pip x1
- Total remaining: 32 (MEDIUM: 26, HIGH: 6)

## Remediated findings

### requests 2.32.3 -> 2.33.0
CVE-2024-47081: .netrc credential leak via malicious redirect URLs.
CVE-2026-25645: Security bypass via predictable temp file creation.
Both fixed by pinning requests==2.33.0 in requirements.txt.

### OpenSSL CVE-2026-28390 (HIGH)
Null pointer dereference in CMS processing, causing denial of service.
Fixed by adding apt-get upgrade to Dockerfile runtime stage, pulling
patched Debian package 3.5.5-1~deb13u2.

### pip 25.0.1 -> 26.0.1 (CVE-2025-8869)
Missing symlink checks during archive extraction.
Fixed by running pip install --upgrade pip in Dockerfile runtime stage.

## Unfixed upstream findings

### CVE-2025-69720 — ncurses (HIGH, 4 packages)
Buffer overflow in terminal UI library. No Debian fix available.
Risk: negligible. LabWatch is a headless HTTP API. ncurses is never
invoked at runtime. Attack requires controlling terminal input to a
running ncurses application.

### CVE-2026-29111 — systemd (HIGH, libsystemd0 + libudev1)
Arbitrary code execution via spurious IPC. No fix available.
Risk: negligible. systemd is not running as PID 1 in this container.
libsystemd0 is a library dependency on disk only. Attack requires an
active systemd process accepting D-Bus connections.

### CVE-2026-4878 — libcap2 (MEDIUM)
TOCTOU race in cap_set_file(). No fix available.
setcap is called at image build time only, not at runtime.
Race window during a controlled build is theoretical.

### Remaining MEDIUM OS findings (23 findings)
Affects: glibc, util-linux, xz, zlib, tar, systemd nspawn/udev.
Status: affected, no fixed version available from Debian.
Attack vectors require local system access, physical hardware, or
direct archive manipulation — none exposed by a Flask HTTP API.

## Remediation policy
Image is rebuilt and rescanned on every dependency update and on any
new CRITICAL or HIGH finding with an available fix. Unfixed findings
are reviewed when Debian security advisories ship patches.
