# Deployment Guide

This guide explains how to deploy ReviewInsight to production.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Internet connection for pulling images

## Quick Start with Docker Compose

### 1. Clone and Setup

```bash
git clone <repository-url>
cd TugasPemWeb3
```

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
POSTGRES_PASSWORD=your_secure_password

# Optional (defaults provided)
POSTGRES_USER=postgres
POSTGRES_DB=review_analyzer
BACKEND_PORT=5000
FRONTEND_PORT=80
```

### 3. Deploy

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows:**
```cmd
deploy.bat
```

**Manual deployment:**
```bash
docker-compose build
docker-compose up -d
```

### 4. Verify Deployment

- Frontend: http://localhost:80
- Backend API: http://localhost:5000/api/health

## Manual Deployment

### Backend Only

```bash
cd backend
docker build -t review-analyzer-backend .
docker run -d \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  -e GEMINI_API_KEY=your_key \
  review-analyzer-backend
```

### Frontend Only

```bash
cd frontend
docker build -t review-analyzer-frontend .
docker run -d -p 80:80 review-analyzer-frontend
```

## Production Considerations

### 1. Environment Variables

Set these in production:

- `FLASK_ENV=production`
- Strong `POSTGRES_PASSWORD`
- Valid API keys for AI services

### 2. Database Backup

```bash
docker-compose exec postgres pg_dump -U postgres review_analyzer > backup.sql
```

### 3. SSL/HTTPS

Use a reverse proxy (nginx/traefik) with SSL certificates for production.

### 4. Scaling

- Backend: Increase `--workers` in Dockerfile
- Database: Use managed PostgreSQL service
- Frontend: Use CDN for static assets

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Health Checks

```bash
# Backend
curl http://localhost:5000/api/health

# Frontend
curl http://localhost:80
```

## Troubleshooting

### Services won't start

1. Check logs: `docker-compose logs`
2. Verify .env file is correct
3. Check port availability: `netstat -an | grep :80`

### Database connection errors

1. Verify PostgreSQL is running: `docker-compose ps postgres`
2. Check DATABASE_URL in .env
3. Ensure database exists

### Build failures

1. Clear Docker cache: `docker-compose build --no-cache`
2. Check disk space: `docker system df`
3. Verify Docker is running: `docker ps`

## Updating

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Stopping Services

```bash
# Stop services (keep data)
docker-compose stop

# Stop and remove containers (keep volumes)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

## Cloud Deployment

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT app:app
   ```
3. Deploy: `git push heroku main`

### AWS/Azure/GCP

Use container services (ECS, AKS, GKE) with docker-compose or Kubernetes manifests.

## Security Checklist

- [ ] Strong database password
- [ ] API keys secured (not in git)
- [ ] HTTPS enabled
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] Logs monitored
- [ ] Updates applied regularly

