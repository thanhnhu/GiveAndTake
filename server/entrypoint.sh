#!/bin/bash

set -e

echo "${0}: running migrations."
#python manage.py makemigrations --merge
#python manage.py migrate --noinput
python manage.py migrate
python manage.py loaddata cities

echo "${0}: collecting statics."

python manage.py collectstatic --noinput

cp -rv static/* static_shared/

# gunicorn yourapp.wsgi:application \
#     --env DJANGO_SETTINGS_MODULE=yourapp.production_settings \
#     --name yourapp \
#     --bind 0.0.0.0:8000 \
#     --timeout 600 \
#     --workers 4 \
#     --log-level=info \
#     --reload