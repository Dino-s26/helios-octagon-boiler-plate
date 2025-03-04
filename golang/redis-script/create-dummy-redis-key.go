package main

import (
	"context"
	"crypto/rand"
	"crypto/tls"
	"encoding/hex"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"

	// external dependencies
	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()

func randomString(length int) string {
	bytes := make([]byte, length)
	_, err := rand.Read(bytes)
	if err != nil {
		panic(err)
	}
	return hex.EncodeToString(bytes)[:length]
}

func main() {
	// Load environment variables from .env file
	err := godotenv.Load(".env") // Mount the ConfigMap here
	if err != nil {
		log.Println("No .env file found, using environment variables from secrets")
	}

	// Command-line flags
	useTLS := flag.Bool("tls", false, "Enable TLS for Redis connection")
	insecureTLS := flag.Bool("insecure", false, "Allow insecure TLS connections")
	flag.Parse()

	// Get Redis connection details
	redisHost := os.Getenv("REDIS_HOST")
	redisPort := os.Getenv("REDIS_PORT")
	redisPassword := os.Getenv("REDIS_PASSWORD")

	redisAddr := fmt.Sprintf("%s:%s", redisHost, redisPort)

	// TLS configuration
	var tlsConfig *tls.Config
	if *useTLS {
		tlsConfig = &tls.Config{
			InsecureSkipVerify: *insecureTLS, // Allow self-signed certificates if insecure mode is set
		}
	}

	client := redis.NewClient(&redis.Options{
		Addr:      redisAddr,
		Password:  redisPassword,
		DB:        0,
		TLSConfig: tlsConfig,
	})

	numKeysStr := os.Getenv("NUM_KEYS")
	numKeys, err := strconv.Atoi(numKeysStr)
	if err != nil {
		numKeys = 100 // Default value
	}

	for i := 0; i < numKeys; i++ {
		key := "test:" + randomString(8)
		value := randomString(20)
		err := client.Set(ctx, key, value, 0).Err()
		if err != nil {
			fmt.Println("Error setting key:", err)
		}
	}

	fmt.Printf("Inserted %d dummy keys into Redis.\n", numKeys)
}
