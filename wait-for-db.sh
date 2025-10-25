#!/bin/sh

# Arguments after script (like uvicorn command) will be passed
CMD="$@"

# Host and port for PostgreSQL
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."

# Wait until PostgreSQL is ready
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - starting FastAPI"
exec $CMD
