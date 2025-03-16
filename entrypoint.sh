#!/bin/bash

# Exit immediately if a command fails
set -e

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    set -a  # Automatically export variables
    source .env
    set +a  # Disable automatic export
else
    echo "⚠️ .env file not found! Ensure it exists in the current directory."
    exit 1
fi

# Validate HOST and PORT environment variables
if [[ -z "${HOST}" || -z "${PORT}" ]]; then
    echo "❌ HOST or PORT environment variable is not set. Please define them in the .env file."
    exit 1
fi

# Validate ENVIRONMENT variable (default to "prod" if not set)
ENVIRONMENT=${ENVIRONMENT:-dev}

# Run FastAPI based on the environment mode
if [[ "$ENVIRONMENT" == "dev" ]]; then
    echo "🚀 Running FastAPI in development mode..."
    fastapi dev app --host "$HOST" --port "$PORT"
else
    echo "🚀 Running FastAPI in production mode..."
    fastapi run app --host "$HOST" --port "$PORT"
fi
