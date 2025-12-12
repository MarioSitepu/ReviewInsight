@echo off
echo Starting Backend Server...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python app.py
pause

