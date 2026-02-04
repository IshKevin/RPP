@echo off
echo Starting RevenuePress AI Setup...

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

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

REM Add PYTHONPATH
set PYTHONPATH=%CD%

echo.
echo Starting Production Server with Waitress...
echo Access the application at http://localhost:8000
echo Press Ctrl+C to stop.
echo.

REM Run with Waitress
waitress-serve --port=8000 --call wsgi:create_app
