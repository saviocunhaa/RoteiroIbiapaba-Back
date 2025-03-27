#!/bin/bash

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput -v 2

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
echo "Starting server..."
gunicorn --bind 0.0.0.0:8000 roteiro_ibiapaba.wsgi:application