@echo off
echo Creating PostgreSQL database...
echo.

cd backend

echo Checking Python virtual environment...
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing psycopg2 if needed...
pip install psycopg2-binary python-dotenv --quiet

echo.
echo Running database creation script...
echo.
python create_database.py

echo.
pause

