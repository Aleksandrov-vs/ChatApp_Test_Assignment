#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

chown www-data:www-data /var/log

exec "$@"