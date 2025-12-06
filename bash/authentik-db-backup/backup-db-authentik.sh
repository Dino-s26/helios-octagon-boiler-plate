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