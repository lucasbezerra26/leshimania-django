#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Starting server"
gunicorn leishimaniaapp.wsgi -c leishimaniaapp/gunicorn.conf.py --log-level info -b 0.0.0.0:8080