#!/bin/sh
DB_HOST=${DB_HOST:-ecommerce-db.internal}
DB_PORT=${DB_PORT:-5432}
echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done
echo "✅ PostgreSQL is up - starting FastAPI"
exec "$@"
