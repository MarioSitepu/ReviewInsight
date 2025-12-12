@echo off
REM Deployment script for ReviewInsight (Windows)

echo Starting deployment...

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo .env file not found. Creating from .env.example...
    copy .env.example .env
    echo Please edit .env file with your configuration before continuing.
    echo Required: GEMINI_API_KEY, POSTGRES_PASSWORD
    pause
)

REM Build and start services
echo Building Docker images...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "Up" >nul
if %ERRORLEVEL% EQU 0 (
    echo Deployment successful!
    echo.
    echo Services status:
    docker-compose ps
    echo.
    echo Frontend: http://localhost:80
    echo Backend API: http://localhost:5000
    echo.
    echo View logs: docker-compose logs -f
    echo Stop services: docker-compose down
) else (
    echo Deployment failed. Check logs with: docker-compose logs
    exit /b 1
)

