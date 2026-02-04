#!/bin/bash

# Exit on error
set -e

echo "Starting RevenuePress AI Setup..."

# Check python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install deps
echo "Installing dependencies..."
pip install -r requirements.txt

# .env check
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

export PYTHONPATH=$PWD

echo ""
echo "Starting Production Server with Gunicorn..."
echo "Access the application at http://localhost:8000"
echo ""

# Run with Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8000 "wsgi:create_app()"
