#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export STATIC_ROOT=/usr/src/app/static/
python manage.py collectstatic --noinput
exec gunicorn samaritan.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3