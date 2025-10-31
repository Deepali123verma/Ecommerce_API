#!/bin/sh
DB_HOST=$(echo $DATABASE_URL | sed -E 's/^.*@([^:\/]+).*/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/^.*:([0-9]+)\/.*/\1/')

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is up - starting FastAPI"
exec "$@"
