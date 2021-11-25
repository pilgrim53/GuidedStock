#!/bin/sh
python manage.py collectstatic -c --no-input

python manage.py migrate

cmd="celery -A GuidedStock worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
$cmd &

gunicorn GuidedStock.wsgi:application -w 2 --bind 0.0.0.0:8000 --reload
