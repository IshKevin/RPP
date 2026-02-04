# Deployment & Execution Guide

This project has been updated to support production deployment and easy local execution.

## 1. Quick Start (Windows)
Double-click `start_server.bat`. 
This will:
- Check for Python.
- Create a virtual environment (`venv`).
- Install all dependencies.
- Start the production server (Waitress) at `http://localhost:8000`.

## 2. Quick Start (Linux/Mac)
Run the script:
```bash
./start_server.sh
```

## 3. Docker Deployment
To run using Docker (recommended for production):
```bash
docker-compose up --build -d
```
The app will be available at `http://localhost:8000`.
Data stays persistent in the `data/` folder and uploads in `app/uploads`.

## 4. Manual Production Setup
If you want to configure it manually on a server:
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set environment variables (see `.env.example`).
4. Run with Gunicorn (Linux):
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 "wsgi:create_app()"
   ```
   Or Waitress (Windows):
   ```bash
   waitress-serve --port=8000 --call wsgi:create_app
   ```
