#!/bin/bash

# Configuration
DAYS_OLD=30
DIRECTORY="."
PREFIX=""
# Default log file in the script's own directory for cron compatibility
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/cleanup.log"

# Logging function
log() {
    local MESSAGE="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$MESSAGE"
    echo "$MESSAGE" >> "$LOG_FILE"
}

# Usage information
usage() {
    echo "Usage: $0 -p <prefix> [-d <directory>] [-n <days>] [-l <logfile>] [-y]"
    echo "  -p: Custom prefix for files to delete (Required)"
    echo "      TIP: Quote your prefix (e.g., -p \"backup-\") to avoid shell expansion."
    echo "  -d: Directory to search in (Default: current directory)"
    echo "  -n: Number of days old (Default: 30)"
    echo "  -l: Path to log file (Default: $LOG_FILE)"
    echo "  -y: Skip confirmation and delete immediately"
    exit 1
}

# Parse arguments
AUTO_CONFIRM=false
while getopts "p:d:n:l:y" opt; do
    case "$opt" in
        p) PREFIX=$OPTARG ;;
        d) DIRECTORY=$OPTARG ;;
        n) DAYS_OLD=$OPTARG ;;
        l) LOG_FILE=$OPTARG ;;
        y) AUTO_CONFIRM=true ;;
        *) usage ;;
    esac
done

if [ -z "$PREFIX" ]; then
    log "Error: Prefix is required."
    usage
fi

if [ ! -d "$DIRECTORY" ]; then
    log "Error: Directory '$DIRECTORY' does not exist."
    exit 1
fi

log "--- Cleanup Configuration ---"
log "Prefix:    $PREFIX"
log "Directory: $DIRECTORY"
log "Age:       > $DAYS_OLD days"
log "Log File:  $LOG_FILE"
log "-----------------------------"

# Find matching files
# Note: Using -name "$PREFIX*" strictly matches the prefix.
# If files don't start with the prefix, they won't be found.
FILES=$(find "$DIRECTORY" -maxdepth 1 -type f -name "$PREFIX*" -mtime +$DAYS_OLD)

# Robust file counting
if [ -z "$FILES" ]; then
    FILE_COUNT=0
else
    FILE_COUNT=$(echo "$FILES" | wc -l | xargs)
fi

if [ "$FILE_COUNT" -eq 0 ]; then
    log "No files found matching the criteria."
    log "Note: Feb 1 to Feb 22 is only 21 days. If you're looking for files from this month, use '-n 20'."
    exit 0
fi

log "Found $FILE_COUNT file(s) to delete:"
while read -r file; do
    if [ -n "$file" ]; then
        log "  - $file"
    fi
done <<< "$FILES"
log "-----------------------------"

if [ "$AUTO_CONFIRM" = true ]; then
    CONFIRM="y"
else
    read -p "Are you sure you want to delete these $FILE_COUNT files? (y/N): " CONFIRM
fi

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    log "Deleting files..."
    while read -r file; do
        if [ -f "$file" ]; then
            rm "$file"
            log "  Deleted: $file"
        fi
    done <<< "$FILES"
    log "Cleanup complete."
else
    log "Operation cancelled."
fi
