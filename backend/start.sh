#!/bin/bash
# Startup script for Render deployment
# This script ensures PORT is set correctly

PORT=${PORT:-5000}

echo "Starting application on port $PORT..."

exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 app:app

