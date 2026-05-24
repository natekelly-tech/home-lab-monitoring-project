#!/bin/bash
# LabWatch Backup Script
# Runs daily via cron. Backs up k3s SQLite state and credential files to Google Drive.
# Backup design documented in LabWatch_Backup_Plan_v1_0.docx

set -euo pipefail

DATE=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%dT%H%M%SZ)
TMP_DIR=/tmp/labwatch-backup
LOG=/var/log/labwatch-backup.log
DB_SOURCE=/var/lib/rancher/k3s/server/db/state.db

echo "[$TIMESTAMP] Starting LabWatch backup" >> "$LOG"

# Create temp working directory
mkdir -p "$TMP_DIR"

# Step 1: k3s SQLite backup
# sqlite3 online backup API handles WAL consistency atomically without stopping k3s
echo "[$TIMESTAMP] Backing up k3s state.db" >> "$LOG"
sqlite3 "$DB_SOURCE" ".backup $TMP_DIR/state-$DATE.db"
gzip "$TMP_DIR/state-$DATE.db"

# Upload to Google Drive
rclone copy "$TMP_DIR/state-$DATE.db.gz" gdrive:LabWatch-Backups/k3s/ \
    --log-file="$LOG" --log-level INFO

echo "[$TIMESTAMP] k3s state backup complete: state-$DATE.db.gz" >> "$LOG"

# Step 2: Credential file backup (weekly on Sunday)
DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" -eq 7 ]; then
    echo "[$TIMESTAMP] Sunday -- running credential backup" >> "$LOG"

    CRED_DIR="$TMP_DIR/credentials-$DATE"
    mkdir -p "$CRED_DIR"

    # Cloudflare tunnel config and credentials
    cp /etc/cloudflared/config.yml "$CRED_DIR/cloudflared-config.yml"
    cp /etc/cloudflared/*.json "$CRED_DIR/" 2>/dev/null || true

    # Certbot Cloudflare API token
    cp /etc/letsencrypt/cloudflare.ini "$CRED_DIR/cloudflare.ini"

    # Full letsencrypt directory as tarball
    tar -czf "$CRED_DIR/letsencrypt-$DATE.tar.gz" /etc/letsencrypt/ 2>/dev/null

    # Upload credential bundle
    rclone copy "$CRED_DIR" "gdrive:LabWatch-Backups/credentials/$DATE/" \
        --log-file="$LOG" --log-level INFO

    echo "[$TIMESTAMP] Credential backup complete" >> "$LOG"
fi

# Step 3: Cleanup temp directory
rm -rf "$TMP_DIR"

echo "[$TIMESTAMP] Backup complete" >> "$LOG"
