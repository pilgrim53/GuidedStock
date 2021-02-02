#!/bin/sh
python manage.py collectstatic -c --no-input

gunicorn pmgstock.wsgi:application --bind 0.0.0.0:8000
