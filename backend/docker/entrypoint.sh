#!/bin/sh
# Apply Django's built-in migrations, then start the development server.
# Postgres can accept connections a moment before it accepts sessions,
# so migrate is retried instead of crashing the container once.
set -eu

attempts=0
until python manage.py migrate; do
  attempts=$((attempts + 1))
  if [ "$attempts" -ge 10 ]; then
    echo "migrate failed after ${attempts} attempts" >&2
    exit 1
  fi
  echo "database not ready, retrying migrate (${attempts})" >&2
  sleep 2
done

exec python manage.py runserver 0.0.0.0:8000
