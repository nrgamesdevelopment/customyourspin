---
description: Repository Information Overview
alwaysApply: true
---

# Custom Your Spin Information

## Summary
A Django-based application for managing advertisements with automatic display functionality. The system provides an admin panel for ad management, automatic ad display, image upload support, and RESTful API endpoints for ad retrieval.

## Structure
- **ads/**: Main application with models, views, admin interface, and templates
- **backend/**: Django project settings and main URL configuration
- **media/**: Uploaded files for local development
- **static/**: Static files (images, CSS, JS)
- **staticfiles/**: Collected static files for production
- **templates/**: HTML templates for the application

## Language & Runtime
**Language**: Python
**Version**: 3.12
**Framework**: Django 5.2.4
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- Django 5.2.4: Web framework
- Pillow 11.3.0: Image processing
- psycopg2-binary: PostgreSQL adapter
- gunicorn: WSGI HTTP server
- whitenoise 6.9.0: Static file serving

## Build & Installation
```bash
# Create virtual environment
python -m venv venv
# Activate virtual environment (Windows)
venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Run migrations
python manage.py migrate
# Create superuser
python manage.py createsuperuser
# Run development server
python manage.py runserver
```

## Docker
**Dockerfile**: Dockerfile
**Base Image**: python:3.12-slim
**Configuration**: 
- Installs dependencies from requirements.txt
- Exposes port 8000
- Runs gunicorn as the web server

## Deployment
**Platform**: Render
**Build Command**: 
```bash
# Build script (build.sh)
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**Start Command**:
```bash
# Start script (start.sh)
python manage.py migrate
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

**Environment Variables**:
- RENDER: Set to "true" for production
- POSTGRES_DB: Database name
- POSTGRES_USER: Database user
- POSTGRES_PASSWORD: Database password
- POSTGRES_HOST: Database host
- POSTGRES_PORT: Database port (default: 5432)
- AWS_ACCESS_KEY_ID: For S3 storage (optional)
- AWS_SECRET_ACCESS_KEY: For S3 storage (optional)
- AWS_STORAGE_BUCKET_NAME: For S3 storage (optional)
- AWS_S3_REGION_NAME: For S3 storage (optional)

## Database
**Development**: SQLite3
**Production**: PostgreSQL (on Render)
**Models**:
- Ad: Stores advertisement information (name, image, link, created_at)

## API Endpoints
- `GET /ads/latest/`: Get the most recent ad
- `GET /ads/all/`: Get all ads
- `GET /admin/`: Admin interface
- `GET /ads/blog/`: Blog index
- `GET /ads/blog/<slug>/`: Blog article

## Issues
The blog templates are missing the `{% load static %}` tag when using `{% static %}` directly in the template. This causes a TemplateSyntaxError. Each template that uses the static tag directly needs to include `{% load static %}` at the top.