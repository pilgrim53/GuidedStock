#!/bin/sh
python manage.py collectstatic -c --no-input

cmd="celery -A pmgstock worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
$cmd &

gunicorn pmgstock.wsgi:application -w 2 --bind 0.0.0.0:8000 --reload
