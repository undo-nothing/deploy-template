#!/usr/bin/env bash

if [ "${SERVICE}" == "web" ]; then
  echo "migrate database"
  python manage.py migrate
  echo "migrate done"
  echo "run web server"
  gunicorn {{ DjangoProject }}.wsgi --worker-class=gevent -b 0.0.0.0:8000 -w 4
fi

if [ "${SERVICE}" == "worker" ]; then
  python manage.py migrate
  echo "run web worker"
  celery -A {{ DjangoProject }} worker --loglevel=ERROR
fi

if [ "${SERVICE}" == "beat" ]; then
  python manage.py migrate
  echo "run web beat"
  celery -A {{ DjangoProject }} beat --schedule=./celery_schedule/celerybeat=schedule --loglevel=ERROR
fi

if [ "${SERVICE}" == "flower" ]; then
  python manage.py migrate
  echo "run web flower"
  celery flower --basic_auth=admin:admin
fi

exec "$@"