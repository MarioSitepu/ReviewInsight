FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with timeout and retry for better reliability
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt --timeout=300

# Install Gunicorn for production
RUN pip install gunicorn

# Copy application code
COPY . .

# Copy and setup start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (Render uses PORT env var, but EXPOSE needs fixed number)
# Render will map external port to internal port automatically
EXPOSE 5000

# Health check (Render will override with its own health check)
# Note: Health check uses fixed port, but app uses $PORT at runtime
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Run with Gunicorn via start script (handles PORT env var)
# Use ENTRYPOINT to ensure script runs properly
ENTRYPOINT ["/bin/bash", "/app/start.sh"]

