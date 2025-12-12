@echo off
setlocal enabledelayedexpansion
echo ========================================
echo PostgreSQL Connection Checker
echo ========================================
echo.

echo [1] Checking if PostgreSQL is installed...
where psql >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] PostgreSQL command-line tools found
    echo.
    echo PostgreSQL version:
    psql --version
) else (
    echo [WARNING] PostgreSQL command-line tools not found in PATH
    echo PostgreSQL may not be installed or not in PATH
    echo.
)

echo.
echo ========================================
echo [2] Checking PostgreSQL Service Status
echo ========================================
echo.

echo Searching for PostgreSQL services...
sc query | findstr /i "postgres" >nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] PostgreSQL services found:
    sc query | findstr /i "postgres"
    echo.
    echo Checking service status...
    for /f "tokens=2" %%a in ('sc query state^= all ^| findstr /i /c:"SERVICE_NAME" ^| findstr /i "postgres"') do (
        set "SERVICE_NAME=%%a"
        echo.
        echo Service: !SERVICE_NAME!
        sc query "!SERVICE_NAME!" | findstr /i "STATE"
    )
) else (
    echo [ERROR] No PostgreSQL services found
    echo.
    echo PostgreSQL is likely NOT installed
    echo.
)

echo.
echo ========================================
echo [3] Testing Connection
echo ========================================
echo.

echo Checking if port 5432 is in use...
netstat -ano | findstr :5432 >nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Port 5432 is in use
    netstat -ano | findstr :5432
) else (
    echo [WARNING] Port 5432 is NOT in use
    echo PostgreSQL is likely NOT running
)

echo.
echo Attempting to connect to PostgreSQL...
where psql >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Testing connection with: psql -U postgres
    echo SELECT version(); | psql -U postgres -d postgres 2>&1 | findstr /v "Password"
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [SUCCESS] Connection test completed
    ) else (
        echo.
        echo [INFO] Connection test requires password input
    )
) else (
    echo [SKIP] Cannot test connection - psql not found
)

echo.
echo ========================================
echo [4] Recommendations
echo ========================================
echo.

where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ACTION REQUIRED] PostgreSQL is not installed
    echo.
    echo To install PostgreSQL:
    echo 1. Download from: https://www.postgresql.org/download/windows/
    echo 2. Run the installer
    echo 3. Set password for 'postgres' user (remember this!)
    echo 4. Use default port 5432
    echo.
    echo See INSTALL_POSTGRESQL_WINDOWS.md for detailed instructions
    echo.
) else (
    netstat -ano | findstr :5432 >nul
    if %ERRORLEVEL% NEQ 0 (
        echo [ACTION REQUIRED] PostgreSQL service is not running
        echo.
        echo To start PostgreSQL:
        echo 1. Press Win+R, type: services.msc
        echo 2. Find PostgreSQL service (postgresql-x64-XX)
        echo 3. Right-click and select "Start"
        echo 4. Or set Startup Type to "Automatic"
        echo.
    ) else (
        echo [OK] PostgreSQL appears to be running
        echo.
        echo Next steps:
        echo 1. Run: create_database.bat
        echo 2. Or manually: psql -U postgres -c "CREATE DATABASE review_analyzer;"
        echo.
    )
)

echo ========================================
echo Diagnostic Complete
echo ========================================
echo.
echo For more help, see:
echo - QUICK_FIX.md (quick solutions)
echo - INSTALL_POSTGRESQL_WINDOWS.md (install guide)
echo - TROUBLESHOOTING_POSTGRESQL.md (detailed troubleshooting)
echo.
pause
