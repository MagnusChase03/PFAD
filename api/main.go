package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	mux := http.NewServeMux()

	fmt.Printf("[LOG] Starting API server on 0.0.0.0:8080.\n")
	if err := http.ListenAndServeTLS("0.0.0.0:8080", "/certs/server.crt", "/certs/server.key", mux); err != nil {
		fmt.Fprintf(os.Stderr, "[ERROR] Failed to start API server. %v\n", err)
	}
}
