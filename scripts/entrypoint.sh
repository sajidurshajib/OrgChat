#!/usr/bin/env bash

cd /app/orgchat

python manage.py collectstatic --noinput
python manage.py migrate --noinput

export DJANGO_SETTINGS_MODULE=orgchat.settings


python -m  gunicorn --bind 0.0.0.0:8000 --workers 3 orgchat.wsgi:application &

daphne -b 0.0.0.0 -p 8001 orgchat.asgi:application
