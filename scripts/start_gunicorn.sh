#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
python manage.py collectstatic --noinput
exec gunicorn samaritan.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
