#!/bin/sh
set -e

# Simple entrypoint: wait for migrations to succeed, then collectstatic and start the CMD
# Retry migrations until they succeed (useful while Postgres is starting)

echo "Starting entrypoint: waiting for DB and applying migrations..."

until python manage.py migrate --noinput; do
  echo "Migrations failed or DB not ready - sleeping 1s"
  sleep 1
done

echo "Migrations applied"

# Collect static files (ignore errors)
python manage.py collectstatic --noinput || true

# Finally exec the container CMD (gunicorn)
exec "$@"
