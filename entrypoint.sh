#!/bin/sh
python manage.py collectstatic -c --no-input

gunicorn pmgstock.wsgi:application -w 2 --bind 0.0.0.0:8000 --reload
