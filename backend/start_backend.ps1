# PowerShell script to start the backend server
Write-Host "Starting Backend Server..." -ForegroundColor Green
Write-Host ""

# Change to backend directory
Set-Location $PSScriptRoot

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$packages = pip list
if ($packages -notmatch "flask") {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start the Flask app
Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "Server will be available at http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
