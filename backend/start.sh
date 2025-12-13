#!/bin/bash
# Startup script for Render deployment
# This script ensures PORT is set correctly

# Get PORT from environment (Render sets this automatically)
PORT=${PORT:-5000}

echo "=========================================="
echo "Starting ReviewInsight Backend"
echo "=========================================="
echo "PORT: $PORT"
echo "Workers: 1 (reduced for memory efficiency)"
echo "Threads: 2"
echo "Timeout: 300s (increased for AI processing)"
echo "Keepalive: 75s"
echo "=========================================="

# Use single worker to reduce memory usage (torch + transformers are heavy)
# Render free tier has limited memory, so we use 1 worker instead of 2
# Increased timeout to 300s because AI model processing can take time
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 2 \
    --timeout 300 \
    --keepalive 75 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    app:app

