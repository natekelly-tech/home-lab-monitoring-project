## 1. Asset Inventory

### Layer 1: AWS Account / IAM
- EC2 instance (i-xxx, t2.small, us-west-1)
- Elastic IP (see SSP v1.1)
- Security Groups (which ports allowed)
- IAM roles attached to EC2 (currently: SSM role, no ec2:CreateImage)
- AWS Backup vaults (none yet)
- S3 buckets (none yet)
- KMS keys (none yet)

### Layer 2: EC2 Host (Ubuntu 24.04)
- Root EBS volume (the disk itself)
- /etc system config (UFW rules, fail2ban jails, sshd_config, cloudflared config)
- /home/ubuntu/repo (working clone of GitHub repo)
- /home/ubuntu/lab (Docker Compose fallback)
- /etc/letsencrypt (TLS certs and Cloudflare API token)
- /etc/cloudflared (tunnel credentials file)
- SSH host keys (/etc/ssh/ssh_host_*)
- systemd unit files for cloudflared
- Installed packages and versions
- Crontabs and timers

### Layer 3: k3s Cluster
- etcd / sqlite datastore (k3s uses sqlite by default unless you configured otherwise)
- Applied manifests (Deployment, Service, ConfigMap, Ingress, HPA)
- Persistent Volumes
- Secrets in the cluster

### Layer 4: Application
- Container image (auxcon/labwatch-api:v0.4.2) - lives on DockerHub
- Application source code - lives in GitHub
- config.py services list
- Any local state the app writes

### Layer 5: External Services
- GitHub repos (homelab-monitoring-project, homelab-app)
- DockerHub images (auxcon/labwatch-api, all tags)
- Cloudflare tunnel
- Cloudflare DNS records for auxcon.dev
- Cloudflare API token (certbot-auxcon)
- Let's Encrypt account
- Porkbun domain registration (auxcon.dev)
- Squarespace domain registration (auxcon.studio)
- Expo / EAS account (njkelly, project ID 5616c167-...)
- Google Play Console account

### Layer 6: Developer Workstation
- SSH private key
- Local git clone of both repos
- Gitleaks pre-commit hook config
- VS Code settings

## 2. Triage: Reconstitutable vs Unique

### Reconstitutable from authoritative source (no backup needed)

| Asset | Why |
|-------|-----|
| Application source code | Stored in GitHub (natekelly-tech/homelab-monitoring-project). Git is the backup. |
| Container image (auxcon/labwatch-api) | Built from source by GitHub Actions and pushed to DockerHub. Rebuild from tag if DockerHub were lost. |
| Mobile app source code | Stored in GitHub (natekelly-tech/homelab-app). |
| k3s manifests (Deployment, Service, ConfigMap, Ingress, HPA) | Committed to git under k8s/. Re-applying them reconstructs cluster desired state. |
| TLS certificate | Let's Encrypt re-issues on demand via Certbot DNS-01. Not unique. |
| Ubuntu OS packages | Re-installable from Ubuntu repos. Not unique. |
| Application runtime state | LabWatch is fully stateless. No database, no history, no file writes. Confirmed via grep and PVC check 2026-05-23. |

### Genuinely unique (backup required)

| Asset | Why | Risk if lost |
|-------|-----|-------------|
| k3s SQLite database (state.db + state.db-shm + state.db-wal) | Contains live cluster state not fully captured by manifest files alone. Includes runtime secrets, service account tokens, and state that diverges from manifests over time. | Must re-apply all manifests and reconfigure from scratch. Recoverable but slow. |
| /etc/cloudflared/config.yml + credentials file | Cloudflare tunnel credentials are generated once at tunnel creation. The credentials file is not in git. | Tunnel is destroyed; must create a new tunnel and update DNS. |
| /etc/letsencrypt/cloudflare.ini | Cloudflare API token for Certbot DNS-01. Not in git (correctly excluded). | Certbot renewal breaks; must regenerate token in Cloudflare dashboard. |
| /etc/letsencrypt/ (full directory) | Private key for TLS cert. Let's Encrypt re-issues certs but cannot re-issue the same private key. | Cert renewal still works; this is lower severity but worth capturing. |
| SSH host keys (/etc/ssh/ssh_host_*) | Identify the server to clients. If lost, every SSH client will show a host key mismatch warning on reconnect. | Recoverable but confusing and requires clearing known_hosts on dev machine. |
| GitHub Actions secrets (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN) | Stored in GitHub, not on EC2. But if GitHub account were compromised and secrets deleted, CI/CD breaks. | Recoverable from DockerHub PAT regeneration. Lower severity. |
| SSH private key (C:\Users\kh4r0\.ssh\id_ed25519) | Lives on dev machine only. If dev machine dies with no backup, EC2 access is lost. | Must add a new key via AWS console recovery. Recoverable but requires console access. |

### Intentionally excluded

| Asset | Reason |
|-------|--------|
| Cloudflare edge config (DNS records, tunnel routing) | Cloudflare is outside the system boundary per SSP Section 1.3. Treated as external dependency. |
| AWS infrastructure config (Security Groups, VPC) | AWS Shared Responsibility Model. AWS backs up control plane state. |
| DockerHub image registry | Outside system boundary. DockerHub provides its own redundancy. |

## 3. Threat Model

Failure modes that backup specifically protects against, distinct from the
security threat table in SSP v1.1.

| ID | Failure Mode | Likelihood | What is lost without backup |
|----|-------------|------------|----------------------------|
| F-01 | EC2 instance or EBS volume failure (AWS hardware or storage failure) | LOW -- AWS provides high durability on EBS, but not 100% | Entire system state. AMI baseline is the primary mitigation. |
| F-02 | Human error on host (destructive command, bad upgrade, config corruption) | MEDIUM -- most common real-world backup trigger in homelab environments | Depends on scope of error. Could be a single config file or the entire cluster state. |
| F-03 | Malicious data destruction following unauthorized access | LOW -- consistent with SSP v1.1 threat assessment | Entire system state. Off-site backup is the only mitigation if attacker has root on EC2. |
| F-04 | Accidental credential loss (Cloudflare token, Certbot config deleted or overwritten) | LOW -- low frequency operations, but high impact if lost | Tunnel access and cert renewal break. System runs but cannot be maintained. |
| F-05 | Developer workstation failure with no SSH key backup | LOW -- single point of failure on dev machine | EC2 access requires AWS console recovery. Recoverable but requires out-of-band action. |

## 4. Recovery Objectives

| Metric | Target | Justification |
|--------|--------|---------------|
| RTO (Recovery Time Objective) | 24 hours | No production SLA exists. No users are operationally dependent on the system as of May 2026. FIPS 199 availability impact is LOW. Downtime overnight causes no material harm. |
| RPO (Recovery Point Objective) | 24 hours | Cluster state is largely static between active development sessions. Credentials and host keys are long-lived and change only on deliberate rotation. Application is fully stateless -- no application data exists to lose regardless of backup age. In practice the true RPO is closer to zero for the unique assets because manifest changes are committed to git before being applied. |

## 5. The 3-2-1 Rule Applied to LabWatch

The 3-2-1 rule: three copies of data, on two different media types, with one
copy off-site.

| Copy | Location | Media type | Notes |
|------|----------|------------|-------|
| Copy 1 | EC2 EBS volume (live system) | Cloud block storage | The running system itself |
| Copy 2 | AWS EBS snapshot / AMI | Cloud snapshot (different from block storage) | Automated via AWS Backup, same region |
| Copy 3 | S3 bucket (us-east-1) | Cloud object storage, different region | k3s state.db export and credential files. Encrypted with KMS. Off-site by virtue of different region. |

Physical media note: traditional 3-2-1 implies tape or external drives for the
off-site copy. For a cloud-native system at LOW impact classification, a
different AWS region with separate failure domain satisfies the intent of the
off-site requirement. True physical media (tape, USB) is not warranted at this
scale and classification level. This decision is documented and accepted.

Developer workstation backup: SSH private key backed up to an encrypted
location separate from the dev machine. Simplest implementation is an
encrypted copy in a password manager or personal cloud storage with strong
passphrase. Covers F-05.

## 6. Backup Type and Rotation Scheme Per Asset

### Background: the three backup types

Full backup: a complete copy of the data at a point in time. Slowest to create,
fastest to restore. You need only one backup to restore.

Incremental backup: captures only what changed since the last backup of any
kind. Fastest to create, slowest to restore. You need the last full backup plus
every incremental since then to restore.

Differential backup: captures only what changed since the last full backup.
Middle ground on both create and restore speed. You need the last full backup
plus the most recent differential to restore.

### Applied to LabWatch unique assets

k3s state.db file export to S3:
- Type: full backup every time.
- Justification: the file is approximately 8MB total (state.db + WAL combined).
  At that size, incremental or differential adds complexity with no meaningful
  time or cost saving. A full copy on every backup run is simpler, faster to
  restore, and easier to verify. Complexity is the enemy of a working backup.

EBS snapshots (via AWS Backup):
- Type: incremental at the block level. AWS manages this automatically.
  The first snapshot is a full copy of the EBS volume. Every subsequent
  snapshot stores only changed blocks since the previous snapshot. Restore
  always produces a full volume regardless of how many incremental snapshots
  are chained. This is transparent to us as operators.
- Justification: AWS EBS incremental snapshots are the industry standard
  approach. We do not need to manage the chain manually.

AMI baseline:
- Type: point-in-time full image, taken manually at major phase milestones.
  Not part of automated rotation. Treated as a stable recovery baseline, not
  a rolling backup.

### GFS Rotation Scheme for EBS Snapshots

GFS stands for Grandfather-Father-Son. It is a rotation scheme that keeps
backups at multiple time horizons without retaining every backup forever.

Applied to LabWatch EBS snapshots via AWS Backup lifecycle policy:

| Generation | Frequency | Retention | Label |
|------------|-----------|-----------|-------|
| Son (daily) | Every 24 hours | 7 days | 7 daily snapshots at any time |
| Father (weekly) | Every Sunday | 4 weeks | 4 weekly snapshots at any time |
| Grandfather (monthly) | First of month | 3 months | 3 monthly snapshots at any time |

Justification: proportionate to LOW impact classification and 24 hour RPO.
Daily snapshots cover the recovery window. Weekly and monthly provide
protection against slowly-discovered errors (corruption noticed a week later,
accidental config deletion not caught for days). Three months of monthly
retention is sufficient for a university course project with no compliance
retention requirement.

Total maximum snapshots at steady state: 7 + 4 + 3 = 14 snapshots.
At t2.small EBS volume sizes this is negligible cost.

## 7. Encryption and Verification

### Encryption decisions

EBS snapshots: encrypted with AWS KMS if the source EBS volume is encrypted.
Need to verify volume encryption status in Session 2 when console access
is confirmed. If volume is not currently encrypted, document as a gap.

S3 bucket for state.db and credential file exports: server-side encryption
with AWS KMS (SSE-KMS). Configured at bucket creation. Justification: the
state.db file contains Kubernetes secrets and service account tokens. The
credential files contain API tokens. These are sensitive at rest and must
be encrypted in the off-site copy. KMS provides key management, audit trail
via CloudTrail, and rotation capability without us managing raw key material.

Encryption in transit: S3 enforces HTTPS for all access. No additional
configuration required.

Developer workstation SSH key backup: encrypted via a password manager or
personal encrypted storage. The passphrase on the key itself provides a
second layer. The backup location must not be the same machine as the key.

### Verification approach

A backup that has never been tested is not a backup. It is an untested hope.
Verification is worth the investment because the restore moment is the worst
possible time to discover the backup is corrupt or incomplete.

Verification plan for LabWatch:

| Asset | Verification method | Frequency |
|-------|-------------------|-----------|
| state.db S3 export | Download from S3, open with sqlite3, run .tables command, confirm tables exist and row counts are non-zero | Monthly or after any cluster change |
| EBS snapshot | Launch a test EC2 instance from the snapshot, confirm k3s starts, confirm kubectl get pods returns expected state, terminate test instance | At major phase milestones |
| AMI baseline | Same as EBS snapshot verification | Once per AMI taken |
| Credential file exports | Download from S3, confirm file is readable, confirm content matches live system | Monthly |

Verification results are logged in the dev log entry for the session in which
the test was run. This constitutes the audit trail for backup integrity.

### Cataloging

At this scale a dedicated catalog tool is not warranted. The catalog is
implicit in two places:

S3 versioning enabled on the backup bucket provides a timestamped object
history for every file stored. This is the catalog for state.db and
credential exports.

AWS Backup console provides a catalog of EBS snapshots with creation time,
source volume, and lifecycle status. This is the catalog for block-level
backups.

Benefit of this approach: the catalog is maintained automatically by the
storage layer. No manual indexing process means no human error in catalog
maintenance and no additional tooling to operate.
