#!/usr/bin/env bash
# Start command for Render deployment

# Apply migrations
python manage.py migrate

# Start gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT 