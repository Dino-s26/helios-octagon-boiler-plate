### How to use 
1. makesure golang already installed
2. init the golang script with `go mod init create-dummy-redis-key.go`
3. on the `.env` file, update the variable for `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` (if using password), `NUM_KEYS` (for the amount of random keys to be generated).
Caution: DO NOT COMMIT YOUR `.env` TO PUBLIC REPOSITORY FOR SECURITY REASON
4. once the `.env` updated, to execute the script, use following command `go run create-dummy-redis-key.go --tls --insecure`
5. check on your redis/valkey for the key generated with `KEYS *`, it should list your dummy key