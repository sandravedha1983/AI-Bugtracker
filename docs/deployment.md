# Deployment Guide

## Render Deployment (Recommended)

1. **Connect Repository**: Link your GitHub repo to a new Render Web Service.
2. **Environment**: Select `Docker` or `Python`.
3. **Environment Variables**: Add all variables from `.env.example`.
4. **Build Command**: `pip install -r requirements.txt` (if using Python environment).
5. **Start Command**: `gunicorn wsgi:app`

## Docker Deployment

Build the image:
```bash
docker build -t ai-bugtracker .
```

Run with Compose:
```bash
docker-compose up -d
```

## Database Initialization
On the first run, ensure you run migrations:
```bash
flask db upgrade
```
The application will automatically seed the admin user on startup if it doesn't exist.
