# Backup script for Authentik Docker

This script purpose are for backup the postgresql Database of Authentik, incase of something happen to the Database
so it can be easily restore upon the Postgresql database failure or any issue related to the database of the Authentik

## Requirement

1. Install Postgresql CLI (Will need the `pg_dumpall` CLI to do the backup)
2. (optional, for offsite backup with S3) AWS CLI

## How to use

1. copy the bash script to the server and save it with `.sh` extension

```
### Adjust as needed like docker name name for the Authentik postgresql, directory to save the backup, etc
#!/bin/sh

## Date Variable

dates=$(date +%d-%m-%y)

echo "-- Begin Authentik DB Backup --"
echo "Timestamp: $(date)"
sleep 3

## Run Backup DB for Authentik DB
echo "--| |--"
echo "Command to run: docker container exec authentik-postgresql-1 pg_dumpall -U authentik -f backup-db-authentik-$dates.sql"
docker container exec authentik-postgresql-1 pg_dumpall -U authentik -f backup-db-authentik-$dates.sql
sleep 3
wait
echo "--| |--"

## Copy DB Data from Container to Host

echo "Command to run: docker container cp authentik-postgresql-1:backup-db-authentik-$dates.sql . "
docker container cp authentik-postgresql-1:backup-db-authentik-$dates.sql . 
sleep 3
wait
echo "--| |--"

## Check current directory for the backup files
## Change the directory with the correct directory 

echo "ls /home/ubuntu/ | grep backup-db-authentik-"
ls -lt /home/ubuntu/ | grep backup-db-authentik-


echo "-- Authentik DB Backup Complete --"
echo "Timestamp: $(date)"
sleep 3
```

2. Make the script executable with following command:

```
chmod +x <script name>.sh

example:
chmod +x backup-db-authentik.sh
```

3. Run the script with following command:

```
./<script name>.sh

example: 
./backup-db-authentik.sh
```

4. (optional) use cron for automatic backup, example like follow:

```
## The following cron will run at 07.30 UTC time each day, adjust as needed
30 07 * * * /home/ubuntu/authentik/./daily-backup-db-authentik-aws.sh >> /home/ubuntu/authentik-backup-log.txt | logger -t "daily backup Authentik DB"
```
