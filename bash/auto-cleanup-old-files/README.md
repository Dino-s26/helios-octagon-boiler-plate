# Auto-Cleanup Old Files

A robust bash script designed to delete files based on a custom prefix and age, with a safety check and logging.

## Features
- **Prefix Matching**: Only targets files starting with a specific string (e.g., `backup-`).
- **Age Filtering**: Targets files older than a specified number of days (default: 30).
- **Pre-deletion Check**: Counts and lists matching files before asking for confirmation.
- **Automated Logging**: Records all actions with timestamps in `cleanup.log` (located in the same directory as the script).
- **Cron Friendly**: Designed to work reliably in scheduled tasks with absolute path logging and an auto-confirm flag.

## Usage

### Basic Command
```bash
./cleanup.sh -p "your-prefix"
```

### Options
- `-p <prefix>`: **(Required)** The prefix of the files to target.
- `-d <directory>`: The directory to search in (Default: current directory).
- `-n <days>`: Delete files older than this many days (Default: 30).
- `-l <logfile>`: Path to a custom log file (Default: `cleanup.log` in script directory).
- `-y`: Auto-confirm (skips the y/n prompt). **Use this for cron jobs.**

### Examples

**Search current directory for files starting with "backup" older than 30 days:**
```bash
./cleanup.sh -p "backup"
```

**Search a specific directory and delete without asking (Dry-run mode not included, but you can run without -y first):**
```bash
./cleanup.sh -p "backup-" -d "/var/backups" -n 60 -y
```

> [!IMPORTANT]
> Always **quote your prefix** (e.g., `-p "backup-"`) to prevent the shell from expanding wildcards before the script runs.

## Cron Setup

To run the cleanup automatically every day at midnight:

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add the following line (using absolute paths):
   ```bash
   0 0 * * * /Users/dino/path/to/cleanup.sh -p "backup-" -d "/path/to/files" -y
   ```

## Configuration (Defaults)
You can edit the top of `cleanup.sh` to set your own permanent defaults for `DAYS_OLD`, `DIRECTORY`, and `PREFIX`.
