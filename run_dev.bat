@echo off
echo Starting RevenuePress AI Development Server...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit /b
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies (quietly to speed up subsequent runs)
echo Checking dependencies...
pip install -r requirements.txt -q

REM Check for .env file
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

REM Add PYTHONPATH
set PYTHONPATH=%CD%

echo.
echo Starting Development Server (Hot-Reload Enabled)...
echo Access the application at http://127.0.0.1:8000
echo Press Ctrl+C to stop.
echo.

REM Run with Flask Dev Server via run.py
python run.py
